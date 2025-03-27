FROM openjdk:21-jdk-slim

WORKDIR /app

COPY build/libs/*[!-plain].jar /app/application.jar

EXPOSE 8080

CMD ["java", "-jar", "application.jar"]
