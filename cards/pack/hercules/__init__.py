from cards.pack import *

GIFT_CARD_IDS = ["59005", "59006", "59007"]
LABOR_CARD_IDS = ["59002", "59003", "59004"]
ALL_VERSUS_ALL = "All Versus All"
APPEAL_TO_ATHENA = "Appeal to Athena"


def GetGiftCount(player: 'Player') -> int:
	# While Appeal to Athena is in this player's obligation area, they control no gifts.
	for face in player.obligations_area.GetAll():
		if face.name == APPEAL_TO_ATHENA:
			return 0
	return len(player.GetControlCards(CardFinder(trait="GIFT")))


def RevealAllVersusAll(effect: 'Effect', player: 'Player|None'=None) -> None:
	scheme = Worlds.FindCardOnField(effect, name=ALL_VERSUS_ALL, card_type=SchemeSide2)
	if scheme:
		return

	found = Search.EncounterCard(
		effect,
		player,
		include_discard_pile=True,
		include_set_aside=True,
		name=ALL_VERSUS_ALL,
		card_type=SchemeSide2,
	)
	if found:
		found.Reveal(player, effect)


def GetTopGiftCard(player: 'Player') -> 'Upgrade|None':
	for face in player.set_aside_deck.Get():
		if face.paper.card_id in GIFT_CARD_IDS:
			return face.CastTo(Upgrade)
	return None


def GetTopLaborCard(player: 'Player') -> 'CardFace|None':
	top = player.additional_deck.GetTop()
	if top and top.paper.card_id in LABOR_CARD_IDS:
		return top
	return None

