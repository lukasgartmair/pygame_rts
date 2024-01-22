#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 17:11:24 2024

@author: lukasgartmair
"""


from goap.action import Action
from goap.planner import RegressivePlanner

def repr_step(step):
    return step.action.__class__.__name__

class BidForBrass(Action):
    effects = {"has_brass": True}
    preconditions = {"has_brass":False, "is_connected": True}
    cost = 1    
    
class GetConnected(Action):
    effects = {"is_connected": True}
    preconditions = {"is_connected": False}
    cost = 1    

class OpponentAI:
    def __init__(self):
        self.state = {
            "is_connected": False,
            "has_brass": False,
        }
        self.goal_state = {"has_brass": True}

        self.actions = [BidForBrass(), GetConnected()]
        self.planner = RegressivePlanner(self.state, self.actions)
        
    # @staticmethod
    # def update_global_action_costs(trading_goods):
        
    #     for a in actions:
    #         if re.split('(?<=.)(?=[A-Z])', a)[-1].lower() in trading_goods:
    #             a.cost = global_assets[]

    def get_plan(self):
        plan = self.planner.find_plan(self.goal_state)
        steps = []
        for i, step in enumerate(plan):
            name = repr_step(step)
            steps.append(name)
        return steps

    def update_state(self, *args):
        self.state = {
            "is_connected": False,
            "has_brass": False,
        }


class KillWithWeapon(Action):
    effects = {"is_killing_it": True}
    preconditions = {"has_weapon": True, "has_ammo": True}
    cost = 1


class Punch(Action):
    effects = {"is_killing_it": True}
    preconditions = {"weapon_in_range": False,
                     "has_weapon": False, "has_ammo": False}
    cost = 20


class GetAmmo(Action):
    effects = {"has_ammo": True}
    preconditions = {"has_weapon": True}
    cost = 2.0


class GetWeapon(Action):
    effects = {"has_weapon": True}
    preconditions = {"weapon_in_range": True}
    cost = 2.0


class GetInWeaponRange(Action):
    effects = {"weapon_in_range": True}
    preconditions = {"weapon_in_range": False}
    cost = 1.0


# if __name__ == "__main__":
#     world_state = {
#         "weapon_in_range": False,
#         "has_weapon": False,
#         "has_ammo": False,
#         "is_killing_it": False,
#     }
#     goal_state = {"is_killing_it": True}
#     print("Initial State:", world_state)
#     print("Goal State:   ", goal_state)

#     actions = [GetWeapon(), GetAmmo(), KillWithWeapon(),
#                GetInWeaponRange(), Punch()]
#     planner = RegressivePlanner(world_state, actions)

#     plan = planner.find_plan(goal_state)
#     print(plan)
