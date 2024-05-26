class CardOrderRepository:
    def __init__(self, db):
        self.collection = db.card_orders

    def find_by_user_id(self, user_id):
        return self.collection.find_one({"user_id": user_id})

    def update_status(self, user_id, status):
        return self.collection.update_one({"user_id": user_id}, {"$set": {"status": status.value}})

    def insert_card_order(self, card_order):
        return self.collection.insert_one(card_order.to_dict())