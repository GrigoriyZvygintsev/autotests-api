import grpc
from concurrent import futures

import course_service_pb2
import course_service_pb2_grpc


class CourseServicer(course_service_pb2_grpc.CourseServiceServicer):
    def GetCourse(self, request, context):
        print(f'Получен запрос для курса id: {request.course_id}')
        return course_service_pb2.GetCourseResponse(course_id=request.course_id,
                                                    title="Автотесты API",
                                                    description="Будем изучать написание API автотестов")

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    course_service_pb2_grpc.add_CourseServiceServicer_to_server(CourseServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('gRPC сервер для курсов запущен на порту 50051...')
    server.wait_for_termination()

if __name__ == '__main__':
    server()