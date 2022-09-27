from pyteal import *

class AnimalHub:
    class Variables:
        name = Bytes("NAME")
        description = Bytes("DESCRIPTION")
        image = Bytes("IMAGE")
        amount = Bytes("AMOUNT")
        adopted = Bytes("ADOPTED")
        address = Bytes("ADDRESS")
        owner = Bytes("OWNER")

    class AppMethods:
        adopt = Bytes("buy")
        release = Bytes("release")
    
    def application_creation(self):
        return Seq([
            Assert(Txn.application_args.length() == Int(5)),
            Assert(Txn.note() == Bytes("animal-hub:uv1")),
            Assert(Btoi(Txn.application_args[3]) > Int(0)),
            App.globalPut(self.Variables.name, Txn.application_args[0]),
            App.globalPut(self.Variables.description, Txn.application_args[1]),
            App.globalPut(self.Variables.image, Txn.application_args[2]),
            App.globalPut(self.Variables.amount, Btoi(Txn.application_args[3])),
            App.globalPut(self.Variables.adopted, Int(0)),
            App.globalPut(self.Variables.address, Global.creator_address()),
            App.globalPut(self.Variables.owner, Txn.application_args[4]),
            Approve()
        ])


    def adopt(self):
        return Seq([
            Assert(
                And(
                    Global.group_size() == Int(2),
                    Txn.application_args.length() == Int(2),
                    App.globalGet(self.Variables.adopted) == Int(0)
                ),
            ),
            Assert(
                And(
                    Gtxn[1].type_enum() == TxnType.Payment,
                    Gtxn[1].receiver() == App.globalGet(
                        self.Variables.address),
                    Gtxn[1].amount() == App.globalGet(self.Variables.amount),
                    Gtxn[1].sender() == Gtxn[0].sender(),
                )
            ),

            App.globalPut(self.Variables.owner, Txn.application_args[1]),
            App.globalPut(self.Variables.address, Gtxn[1].sender()),
            App.globalPut(self.Variables.adopted, Int(1)),
            Approve()
        ])

    def release(self):
        Assert(
            And(
                Txn.application_args.length() == Int(2),
                App.globalGet(
                    self.Variables.owner) == Txn.application_args[1]
            ),
        )

        return Seq([
            App.globalPut(self.Variables.adopted, Int(0)),
            Approve()
        ])

    def application_deletion(self):
        return Return(Txn.sender() == Global.creator_address())

    def application_start(self):
        return Cond(
            [Txn.application_id() == Int(0), self.application_creation()],
            [Txn.on_completion() == OnComplete.DeleteApplication,
             self.application_deletion()],
            [Txn.application_args[0] == self.AppMethods.adopt, self.adopt()],
            [Txn.application_args[0] == self.AppMethods.release, self.release()],
        )

    def approval_program(self):
        return self.application_start()

    def clear_program(self):
        return Return(Int(1))





