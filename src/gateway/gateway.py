class Gateway:
    @staticmethod
    def send(user_id: str, message: str):
        print(f'Sending message {message} to user {user_id}')
