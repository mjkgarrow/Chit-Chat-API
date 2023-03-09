from main import db


member_association = db.Table("members",
                              # The ID of the chat
                              db.Column("chat_id",
                                        db.ForeignKey("chats.id"),
                                        nullable=False),

                              # The ID of the user
                              db.Column("user_id",
                                        db.ForeignKey("users.id"),
                                        nullable=False))
