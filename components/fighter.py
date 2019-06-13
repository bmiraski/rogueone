class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        self.hp -= amount

    def attack(self, target):
        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
            print(f'''{self.owner.name.capitalize()} attacks {target.name} for {
                  str(damage)} hit points.''')

        else:
            print(f'''{self.owner.name.capitalize()} attacks {
                  target.name} but does no damage.''')
