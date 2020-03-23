from optimizer import Optimizer
import config
import json


def main():
    with open(config.DROP_SUMMARY, 'r') as f:
        drop_summary = json.load(f)

    with open(config.COMBINE_TRANSFORM, 'r') as f:
        combine_transform = json.load(f)

    with open(config.RESPAWN_ITEMS, 'r') as f:
        respawn_items = json.load(f)

    with open(config.REQUIREMENT_ITEMS, 'r') as f:
        requirement_items = json.load(f)

    with open(config.STORED_ITEMS, 'r') as f:
        stored_items = json.load(f)

    with open(config.CERT_TRANSFORM, 'r') as f:
        cert_transform = json.load(f)

    for k in stored_items:
        requirement_items[k] = requirement_items.get(k, 0) - stored_items[k]

    print('== Requirement ==')
    print(requirement_items)

    model = Optimizer(drop_summary, combine_transform, cert_transform, respawn_items, requirement_items)
    model.solve()
    print('Status: ', model.status)

    print('== Solution ==')
    for v in sorted(model.variables, key=lambda v: -v.varValue):
        if v.varValue > 1e-5:       # ignore unused (= inefficient) actions
            print(v.name, '=', v.varValue)

    print('== Detail ==')
    # for item in requirement_items:
    for item in requirement_items:
        print(item)
        detail = model.item_detail(item)
        total = 0.0
        for v, coeff in detail:
            print('\t{} : {:.2f} * {:.2f} = {:.2f}'.format(v.name, v.varValue, coeff, v.varValue * coeff))
            total += v.varValue * coeff
        print('Total : {:.2f}'.format(total))
        print('Surplus : {:.2f}'.format(total - requirement_items[item]))


if __name__ == '__main__':
    main()
