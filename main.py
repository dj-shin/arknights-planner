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

    print('== Requirement ==')
    print(requirement_items)

    model = Optimizer(drop_summary, combine_transform, respawn_items, requirement_items)
    model.solve()
    print('Status: ', model.status)

    print('== Solution ==')
    for v in sorted(model.variables, key=lambda v: -v.varValue):
        if v.varValue > 1e-5:       # ignore unused (= inefficient) actions
            print(v.name, '=', v.varValue)


if __name__ == '__main__':
    main()
