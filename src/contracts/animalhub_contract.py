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
            # checks if there are any empty values in application_args
            Assert(
                And(
                    Txn.note() == Bytes("animal-hub:uv1"),
                    Txn.application_args.length() == Int(5),
                    Btoi(Txn.application_args[3]) > Int(0),
                    Len(Txn.application_args[0]) > Int(0),
                    Len(Txn.application_args[1]) > Int(0),
                    Len(Txn.application_args[2]) > Int(0),
                    Len(Txn.application_args[4]) > Int(0)
                ),
            ),
            App.globalPut(self.Variables.name, Txn.application_args[0]),
            App.globalPut(self.Variables.description, Txn.application_args[1]),
            App.globalPut(self.Variables.image, Txn.application_args[2]),
            App.globalPut(self.Variables.amount, Btoi(Txn.application_args[3])),
            App.globalPut(self.Variables.adopted, Int(0)),
            App.globalPut(self.Variables.address, Global.creator_address()),
            App.globalPut(self.Variables.owner, Txn.application_args[4]),
            Approve()
        ])

    # allow users to adopt an animal that is up for adoption
    # user must also sends a payment transaction matching the amount required to adopt the animal
    def adopt(self):
        return Seq([
            # checks if there are 2 transactions in this transaction group(adopt transaction and payment transaction)
            # checks if the new owner(application_args[1]) is not an empty value
            # checks if animal is up for adoption
            Assert(
                And(
                    Global.group_size() == Int(2),
                    Txn.application_args.length() == Int(2),
                    Len(Txn.application_args[1]) > Int(0),
                    App.globalGet(self.Variables.adopted) == Int(0),
                    App.globalGet(self.Variables.address) != Txn.sender(),
                ),
            ),
            # checks if receiver of payment is the current animal's owner
            # checks if the amount sent matches the amount required to adopt the animal
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

        # checks if it is the sender of the transaction is the owner of the animal
        Assert(
            And(
                Txn.application_args.length() == Int(2),
                App.globalGet(self.Variables.owner) == Txn.application_args[1],
                App.globalGet(self.Variables.address) == Txn.sender(),
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





