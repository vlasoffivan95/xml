import xml.etree.ElementTree as ET
from collections import Counter

class Manager:
    def __init__(self, name, email, phone, clients):
        self.name = name
        self.email = email
        self.phone = phone
        self.clients = clients

    def __str__(self):
        return 'Manager: name={}, clients={} '.format(self.name, self.clients)

    def sumOfClosedCredits(self):
        total = 0
        for client in self.clients:
            for action in client.actions:
                if action.isActive == False:
                    total += action.value
        return total

class Client:
    def __init__(self, id, name, actions):
        self.id = id
        self.name = name
        self.actions = actions

    def __str__(self):
        return 'Client: id={}, name={}, actions={} '.format(self.id, self.name, self.actions)

    def balanceSumOfActiveCredit(self):
        creditsSum = 0
        paysSum = 0
        for action in self.actions:
            if action.isCredit == True and action.isActive:
                creditsSum += action.value
                for pay in action.pays:
                    paysSum += pay.value
        return creditsSum - paysSum

class BankAction: #credit, deposit
    def __init__(self, isCredit, isActive, value, pays):
        self.isCredit = isCredit
        self.isActive = isActive
        self.value = value
        self.pays = pays

    def __str__(self):
        return 'BankAction isCredit={}, isActive={}, value={}, pays={}'.format(self.isCredit, self.isActive, self.value, self.pays)

class Pay:
    def __init__(self, value, date):
        self.value = value
        self.date = date

    def __str__(self):
        return 'Pay value={}, date={}'.format(self.value, self.date)




class Parser:
    def __init__(self, root):
        self.managers = []      # [Managers]
        for manager in root:
            clients = []        # [Clients]
            for client in manager:
                actions = []    # [BankAction]
                for action in client:
                    pays = []   # [Pay]
                    for pay in action:
                        payItem = Pay(float(pay.attrib['value']),
                                      pay.attrib['date'])
                        pays.append(payItem)

                    actionItem = BankAction(action.tag == 'credit',
                                            action.attrib['status'] == 'active',
                                            float(action.attrib['value']),
                                            pays)
                    actions.append(actionItem)

                clientItem = Client(client.attrib['id'],
                                    client.attrib['name'],
                                    actions)
                clients.append(clientItem)

            managerItem = Manager(manager.attrib['name'],
                                  manager.attrib['email'],
                                  manager.attrib['phone'],
                                  clients)
            self.managers.append(managerItem)

    #1
    def topClient(self):
        topClient = self.managers[0].clients[0]
        for manager in self.managers:
            for client in manager.clients:
                if client.balanceSumOfActiveCredit() > topClient.balanceSumOfActiveCredit():
                    topClient = client
        return topClient

    #2
    def topManagers(self):
        topManagers = sorted(self.managers, key=lambda x: -x.sumOfClosedCredits())
        return topManagers[:3]

    #3
    def avgSumOfActiveDeposit(self):
        result = 0
        count = 0
        for manager in self.managers:
            for client in manager.clients:
                for action in client.actions:
                    if action.isActive == True and action.isCredit == False:
                        result += action.value
                        count += 1
        return result / count



tree = ET.parse('bank.xml')
root = tree.getroot()

parser = Parser(root)

print('#1:')
print(' top client = {} ({})'.format(parser.topClient().name, parser.topClient().balanceSumOfActiveCredit()))

print('#2:')
for item in parser.topManagers():
    print(' {} = {}'.format(item.name, item.sumOfClosedCredits()))

print('#3:')
print(' avg sum of all active deposits = {}'.format(parser.avgSumOfActiveDeposit()))