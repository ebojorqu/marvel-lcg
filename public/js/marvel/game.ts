import { WorldDescriptor } from './descriptor.js'
import { ClassName } from './class_name.js'
import { Message } from './message.js'
import { Cards } from './cards.js';
import { HoverCard } from './hover.js';


// Define the structure for the statistics data
interface PlayerStats {
    id: number;
    damage_dealt?: number;
    damage_taken?: number;
    thwarted_threat?: number;
    entered_play?: number;
    owner_id?: number;
    card_id?: string;
    name?: string;
    set_name?: string;
}

interface StatsRow extends PlayerStats {
    row_type: 'player_total' | 'card_group';
    player_index?: number;
    owner_label?: string;
    pack_label?: string;
    label?: string;
    count?: number;
}

type StatKey = 'damage_dealt' | 'damage_taken' | 'thwarted_threat' | 'entered_play'

const STAT_KEYS: StatKey[] = ['damage_dealt', 'damage_taken', 'thwarted_threat', 'entered_play']

function normalizeName(text: string | undefined): string {
    return (text || '').replace(/^\*\s*/, '').trim()
}

function normalizePack(text: string | undefined): string {
    return (text || '').trim()
}

class GameStatistics {
    static readonly TABLE_BUILD_STAMP = 'Victory Stats v2';
    static currentStats: StatsRow[] = [];
    static sortKey: string | null = null;
    static sortDirection: 'asc' | 'desc' = 'asc';

    static tableElement = document.getElementById('session-statistics') as HTMLTableElement;
    /**
     * Fetches statistics from the backend and converts the dictionary 
     * into an array of PlayerStats objects.
     */
    static async fetchStatistics() {
        try {
            const response = await fetch('/get_session_statistics');
            if (!response.ok) {
                throw new Error('Failed to fetch statistics');
            }
            
            const rawData = await response.json();
            
            // Convert the backend dictionary {player_id: stats_dict} 
            // into an array [{id: player_id, ...stats}]
            const rawStats = Object.entries(rawData).map(([id, stats]) => ({
                id: parseInt(id), // Ensure ID is a number
                ...(stats as Record<string, number>) // Spread the stats
            })) as PlayerStats[];

            GameStatistics.currentStats = GameStatistics.buildRows(rawStats)

            GameStatistics.renderTable();

        } catch (error) {
            console.error("Error fetching session statistics:", error);
            // Display an error message in the table area
            const table = document.getElementById('session-statistics');
            if (table) {
                table.innerHTML = '<tr><td colspan="4">Error loading statistics.</td></tr>';
            }
        }
    }

    static renderTable() {
        
        if (!GameStatistics.tableElement || GameStatistics.currentStats.length === 0) {
            if (GameStatistics.tableElement) GameStatistics.tableElement.innerHTML = '<tr><td>No statistics available.</td></tr>';
            return;
        }

        // Determine headers dynamically from the first player's stats
        const headers: ('id' | StatKey)[] = [
            'id',
            'damage_dealt',
            'damage_taken',
            'thwarted_threat',
            'entered_play',
        ];
        
        // Clear the existing table content
        GameStatistics.tableElement.innerHTML = '';

        // Create the table header (<thead>)
        const thead = GameStatistics.tableElement.createTHead();
        const headerRow = thead.insertRow();
        
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = GameStatistics.formatHeader(headerText);

            if (headerText === 'id') {
                th.textContent += ` (${GameStatistics.TABLE_BUILD_STAMP})`
            }

            th.dataset.key = headerText; // Store the original key for sorting
            th.addEventListener('click', () => GameStatistics.handleSort(headerText));
            
            // Add sorting indicator (optional visual enhancement)
            if (GameStatistics.sortKey === headerText) {
                th.textContent += GameStatistics.sortDirection === 'asc' ? ' ▲' : ' ▼';
            }
            
            headerRow.appendChild(th);
        });

        // Create the table body (<tbody>)
        const tbody = GameStatistics.tableElement.createTBody();
        GameStatistics.currentStats.forEach(stats => {
            const row = tbody.insertRow();
            row.classList.add(stats.row_type === 'player_total' ? 'player-total-row' : 'card-group-row')
            headers.forEach(key => {
                const cell = row.insertCell();
                if (key === 'id') {
                    if (stats.row_type === 'player_total') {
                        cell.textContent = stats.label || 'Player Total'
                    } else {
                        const card = Cards.getCard(stats.id);
                        if (card && card.pic_id !== undefined) {
                            const img = document.createElement('img');
                            img.src = card.pic_id; // Adjust the path as needed
                            img.alt = `${card.pic_id}`; // Add alt text for accessibility
                            img.style.width = '50px'; // Adjust size as needed
                            img.style.height = 'auto';
                            cell.appendChild(img);

                            const meta = document.createElement('div')
                            meta.className = 'session-card-group-meta'

                            const name = document.createElement('div')
                            name.className = 'session-card-group-name'
                            name.textContent = stats.label || card.name

                            const subtitle = document.createElement('div')
                            subtitle.className = 'session-card-group-subtitle'
                            const subtitleText = stats.owner_label || stats.pack_label || ''
                            if (subtitleText && subtitleText !== 'Unknown') {
                                subtitle.textContent = subtitleText
                            } else {
                                subtitle.style.display = 'none'
                            }

                            meta.appendChild(name)
                            meta.appendChild(subtitle)
                            cell.appendChild(meta)

                            const title = document.createElement('div')
                            title.className = 'session-card-group-title'
                            const copyText = stats.count && stats.count > 1 ? `${stats.count}x` : ''
                            title.textContent = copyText
                            cell.appendChild(title)

                            cell.onmouseenter = () => {
                                HoverCard.showLogImage(stats.id, card.pic_id)
                            }
                        } else {
                            cell.textContent = 'No Image'; // Handle cases where card or pic_id is missing
                        }
                    }
                } else {
                    cell.textContent = (stats[key as StatKey] ?? 0).toString();
                }
            });
        });
    }

    static buildRows(rawStats: PlayerStats[]): StatsRow[] {
        const playerRowsMap = new Map<number, StatsRow>()
        const groupRowsMap = new Map<string, StatsRow>()

        let maxOwnerId = -1
        for (const stats of rawStats) {
            if ((stats.owner_id ?? -1) > maxOwnerId) {
                maxOwnerId = stats.owner_id ?? -1
            }
        }

        const worldPlayers = Game.world_descriptor?.players?.length ?? 0
        const totalPlayers = Math.max(worldPlayers, maxOwnerId + 1)
        for (let playerIndex = 0; playerIndex < totalPlayers; playerIndex++) {
            const playerIdentity = Game.world_descriptor?.players?.[playerIndex]?.area_hero?.[0]
            const fallbackHero = rawStats.find(x =>
                (x.owner_id ?? -1) === playerIndex &&
                !!x.card_id &&
                /[ab]$/i.test(x.card_id) &&
                !!x.name
            )
            const playerName = normalizeName(playerIdentity?.name) || normalizeName(fallbackHero?.name) || `Player ${playerIndex + 1}`
            playerRowsMap.set(playerIndex, {
                id: -1 - playerIndex,
                row_type: 'player_total',
                player_index: playerIndex,
                label: `P${playerIndex + 1} (${playerName})`,
                damage_dealt: 0,
                damage_taken: 0,
                thwarted_threat: 0,
                entered_play: 0,
            })
        }

        for (const stats of rawStats) {
            const damageDealt = stats.damage_dealt ?? 0
            const damageTaken = stats.damage_taken ?? 0
            const thwartedThreat = stats.thwarted_threat ?? 0
            // Keep rows out if they only contributed entered_play.
            if (damageDealt === 0 && damageTaken === 0 && thwartedThreat === 0) {
                continue
            }

            const card = Cards.getCard(stats.id)
            const ownerIndex = stats.owner_id ?? card?.control_player ?? -1
            const ownerName = ownerIndex >= 0
                ? (normalizeName(Game.world_descriptor?.players?.[ownerIndex]?.area_hero?.[0]?.name) || `Player ${ownerIndex + 1}`)
                : 'Unknown'
            const ownerLabel = ownerIndex >= 0 ? `P${ownerIndex + 1} (${ownerName})` : 'Unknown'
            if (ownerIndex >= 0 && playerRowsMap.has(ownerIndex)) {
                const ownerRow = playerRowsMap.get(ownerIndex)!
                for (const statKey of STAT_KEYS) {
                    ownerRow[statKey] = (ownerRow[statKey] ?? 0) + (stats[statKey] ?? 0)
                }
            }

            const cardName = normalizeName(stats.name || card?.name || `Card ${stats.id}`)
            const cardPack = normalizePack(stats.set_name || Cards.getCardPackName(stats.id))
            const cardIdentity = (stats.card_id || card?.card_id || String(stats.id)).replace(/[ab]$/i, '')
            const groupKey = `${cardName.toLowerCase()}||${cardPack.toLowerCase()}||${cardIdentity}||${ownerIndex}`
            if (!groupRowsMap.has(groupKey)) {
                groupRowsMap.set(groupKey, {
                    id: stats.id,
                    row_type: 'card_group',
                    label: cardName,
                    owner_label: ownerLabel,
                    pack_label: cardPack || 'Unknown',
                    count: 0,
                    damage_dealt: 0,
                    damage_taken: 0,
                    thwarted_threat: 0,
                    entered_play: 0,
                })
            }

            const groupRow = groupRowsMap.get(groupKey)!
            groupRow.count = (groupRow.count ?? 0) + 1
            for (const statKey of STAT_KEYS) {
                groupRow[statKey] = (groupRow[statKey] ?? 0) + (stats[statKey] ?? 0)
            }
        }

        const playerRows = [...playerRowsMap.entries()]
            .sort((a, b) => a[0] - b[0])
            .map(([, row]) => row)

        const groupedRows = [...groupRowsMap.values()]
            .sort((a, b) => {
                const nameCompare = (a.label || '').localeCompare(b.label || '')
                if (nameCompare !== 0) {
                    return nameCompare
                }
                return (b.damage_dealt ?? 0) - (a.damage_dealt ?? 0)
            })

        return [...playerRows, ...groupedRows]
    }

    /**
     * Utility function to format the header text (e.g., 'damage_dealt' to 'Damage Dealt').
     */
    static formatHeader(text: string): string {
        return text.replace(/_/g, ' ')
                .replace(/\b\w/g, char => char.toUpperCase());
    }

    // --- Sorting Logic ---

    /**
     * Handles the sorting of the data when a header is clicked.
     */
    static handleSort(key: string) {
        if (GameStatistics.sortKey === key) {
            // If the same header is clicked, toggle the direction
            GameStatistics.sortDirection = GameStatistics.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            // If a new header is clicked, set the new key and default to ascending
            GameStatistics.sortKey = key;
            GameStatistics.sortDirection = 'desc';
        }

        // Sort the current data array
        const playerRows = GameStatistics.currentStats.filter(row => row.row_type === 'player_total')
        const groupedRows = GameStatistics.currentStats.filter(row => row.row_type === 'card_group')

        groupedRows.sort((a, b) => {
            if (key === 'id') {
                const valueA = a.label ?? ''
                const valueB = b.label ?? ''
                if (valueA < valueB) {
                    return GameStatistics.sortDirection === 'asc' ? -1 : 1;
                }
                if (valueA > valueB) {
                    return GameStatistics.sortDirection === 'asc' ? 1 : -1;
                }
                return 0;
            }

            const statKey = key as StatKey
            const valueA = a[statKey] ?? 0;
            const valueB = b[statKey] ?? 0;
            
            if (valueA < valueB) {
                return GameStatistics.sortDirection === 'asc' ? -1 : 1;
            }
            if (valueA > valueB) {
                return GameStatistics.sortDirection === 'asc' ? 1 : -1;
            }
            return 0;
        });

        GameStatistics.currentStats = [...playerRows, ...groupedRows]

        // Re-render the table with the sorted data
        GameStatistics.renderTable();
    }

}

///////////////////////////////////////////////////////////////////////////////
// Game
export class Game {
    static game_over = false
    static players_won = false
    static is_pause = false
    static is_lost_connect = true
    static forced_on_player = -1 // [-1, 0~3]
    // static current_player = 0 // 0, 1, 2, 3
    static total_players = 1
    static asking_players: number[] = [] // 0,1,2,3
    static current_step_id = -1

    static world_descriptor: WorldDescriptor

    static setGameOver(game_over: boolean) {
        if( Game.game_over != game_over ) {
            Game.game_over = game_over
            if( Game.game_over ) {
                document.body.classList.add(ClassName.game_over)
                console.log('Game over')
            } else {
                document.body.classList.remove(ClassName.game_over)
                GameStatistics.tableElement.innerHTML = '';
                document.getElementById('game-over-box-container')!.classList.remove('minimize')
                Message.cleanGameOverMessage()
            }

            if( Game.game_over ) {
                setTimeout(async () => {
                    await GameStatistics.fetchStatistics()
                    GameStatistics.renderTable()
                }, 1000);
            }
        }
    }
}

(window as any).Game = Game;

