FROM openjdk:8-jdk-alpine
VOLUME /tmp
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} idgen-0.1.jar
ENTRYPOINT ["java","-Dserver.servlet.context-path=/uuid -Djava.security.egd=file:/dev/./urandom","-jar","/idgen-0.1.jar"]
