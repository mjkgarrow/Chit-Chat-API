from main import db


likes_association = db.Table("likes",
                             # The ID of the message
                             db.Column("message_id",
                                       db.ForeignKey("messages.id"),
                                       nullable=False),

                             # The ID of the user
                             db.Column("user_id",
                                       db.ForeignKey("users.id"),
                                       nullable=False))
