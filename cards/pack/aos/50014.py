from . import *

# Organizational Support

MAX_EXHAUST = 3

def GetAbilities() -> Sequence['Ability']:

    # Only `MAX_EXHAUST` cards can be exhausted, so pick the ones that fit the cost best
    def pick_faces(faces: List['CardFace'], cost: 'Cost') -> List['CardFace']:
        needed_colors = [x for x in ("R", "B", "Y") if cost.rbyga.rbyg.GetColor(x, convert_green_res=False) > 0]

        def priority(face: 'CardFace') -> int:
            res = face.CastTo(ClassCard).printed_resource
            if any(res.HasColorPrinted(x) for x in needed_colors):
                return 0
            if res.HasColorPrinted("G"):
                return 1
            return 2

        return sorted(faces, key=priority)[:MAX_EXHAUST]

    def organizational_support(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        this = effect.this.CastTo(Resource)
        Unused(this)

        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        faces = initiator.GetControlCardsByType(CardFinder(canbe_exhaust=True, share_trait=identity), ally=True, support=True)
        return FacesCounter.GetPrintedResources([this] + pick_faces(faces, message.cost))

    def organizational_support_res(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> 'Resources':
        this = effect.this.CastTo(Resource)
        Unused(this)

        faces = effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards
        return FacesCounter.GetPrintedResources([this] + faces)

    return [
        AbilityFactory.DoDiscardThisToGenerateResources(
            AbilityType.Interrupt,
            res_fn=organizational_support_res,
        ).SetCostFunc(CostFunc.Exhaust(
            card_type=Support|Ally,
            share_trait_with_your_identity=True,
            from_where=["YouControlCards"],
            range=(0, MAX_EXHAUST))),
        AbilityFactory.CheckThisCanDropPay(
            organizational_support,
        ),
    ]

