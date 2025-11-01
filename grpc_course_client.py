import grpc

import course_service_pb2
import course_service_pb2_grpc

def run_client():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = course_service_pb2_grpc.CourseServiceStub(channel)
        request = course_service_pb2.GetCourseRequest(course_id='api-course')
        response = stub.GetCourse(request)
    print("Ответ от сервера:")
    print(response)

if __name__ == '__main__':
    run_client()
