import requests
import json

import config


def get_drops(stage_id, item_name_map):
    url = 'https://penguin-stats.io/PenguinStats/api/result/stage/{}'.format(stage_id)
    resp = requests.get(url)
    data = resp.json()
    stage_name = data['stage']['code']
    drops = data['drops']
    cost = data['stage']['apCost']
    result = {
        '이성': -cost
    }
    for drop in drops:
        times = drop['times']
        quantity = drop['quantity']
        name = drop['item']['name_i18n']['en']
        if item_name_map.get(name) is not None:
            name = item_name_map[name]
        result[name] = quantity / times
    return stage_name, result


def crawl():
    stages = {
        'main': {0: 11, 1: 12, 2: 10, 3: 8, 4: 10, 5: 10},
        'sub': {2: 12, 3: {1: 2, 2: 3, }, 4: {1: 3, 2: 3, 3: 3, 4: 1, }, 5: {1: 2, 2: 2, 3: 2, 4: 2}}
    }

    with open(config.ITEM_NAME_MAP, 'rt') as f:
        item_name_map = json.load(f)

    stage_ids = list()
    for zone in stages:
        for area in stages[zone]:
            detail = stages[zone][area]
            if isinstance(detail, int):
                for i in range(detail):
                    name = '{}_{:02d}-{:02d}'.format(zone, area, i + 1)
                    stage_ids.append(name)
            else:
                for high in detail:
                    low = detail[high]
                    for i in range(low):
                        name = '{}_{:02d}-{}-{}'.format(zone, area, high, i + 1)
                        stage_ids.append(name)

    # GT event area
    # stage_ids += ['a001_{:02d}'.format(i + 1) for i in range(6)]
    # stage_ids += ['a003_{:02d}'.format(i + 1) for i in range(8)]
    # stage_ids += ['a003_f{:02d}'.format(i + 1) for i in range(4)]

    actions = list()
    summary = dict()

    for stage_id in stage_ids:
        stage_name, drops = get_drops(stage_id, item_name_map)
        actions.append(stage_name)
        summary[stage_name] = drops

    with open(config.DROP_SUMMARY, 'w', encoding='UTF-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)


if __name__ == '__main__':
    crawl()
