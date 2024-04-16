import httpx


# class RequestService:
#     @staticmethod
#     def make_request(*args, **kwargs):
#         with httpx.AsyncClient() as client:
#             client.request(
#                 *args,
#                 **kwargs,
#             )
#
#
# class JwtService(RequestService):
#     def get_jwt(self, data):
#         self.make_request(method="POST", body=data)

# with httpx.AsyncClient() as client:
#    client.post()


# Partition 1 <- Consumer A
# Partition 2 <- Consumer B
# Partition 3 <- Consumer C
# Partition 3 <- Consumer D

# Partition Message <- Consumer C & Consumer D (Data Race Problem)
