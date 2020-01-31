import pulp
import config
import json


class Optimizer:
    def __init__(self, drop_summary, combine_transform, respawn_items, requirement_items):
        with open(config.ITEM_LIST, 'r') as f:
            resources = json.load(f)['items']
        self.resources = resources
        self.validate(drop_summary, combine_transform, respawn_items, requirement_items)

        self.drop_summary = drop_summary
        self.combine_transform = combine_transform
        self.respawn_items = respawn_items
        self.requirement_items = requirement_items

        area_actions = list(drop_summary.keys())
        combine_actions = list(combine_transform.keys())
        self.actions = area_actions + combine_actions

        # generate matrix / vectors
        self.transform = [[drop_summary[action].get(resource, 0) for resource in resources] for action in area_actions]
        self.transform += [[-combine_transform[outcome].get(resource, 0.0) if outcome != resource else 1.0
                           for resource in resources] for outcome in combine_actions]
        self.respawn = [respawn_items.get(resource, 0.0) for resource in resources]
        self.requirement = [requirement_items.get(resource, 0.0) for resource in resources]

        self._model = pulp.LpProblem('Resource optimization', pulp.LpMinimize)

    def validate(self, drop_summary, combine_transform, respawn_items, requirement_items):
        resources = self.resources
        # drops
        for drop in drop_summary.values():
            for key in drop:
                assert key in resources, 'Invalid item: {}'.format(key)

        # combine transform
        for output_item, input_items in combine_transform.items():
            assert output_item in self.resources, 'Invalid item: {}'.format(output_item)
            for input_item in input_items:
                assert input_item in resources, 'Invalid item: {}'.format(input_item)

        # respawn
        for key in respawn_items:
            assert key in resources, 'Invalid item: {}'.format(key)

        # requirements
        for key in requirement_items:
            assert key in resources, 'Invalid item: {}'.format(key)

    def solve(self):
        t = pulp.LpVariable('Time', lowBound=0)

        vec = [pulp.LpVariable(action, lowBound=0) for action in self.actions]

        self._model += t    # objective function: minimize t
        for j in range(len(self.resources)):
            self._model += t * self.respawn[j] +\
                    sum([vec[i] * self.transform[i][j] for i in range(len(self.actions))]) >= self.requirement[j]

        self._model.solve()

    @property
    def status(self):
        return pulp.LpStatus[self._model.status]

    @property
    def variables(self):
        return self._model.variables()
