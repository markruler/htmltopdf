version = 0.9.0
image_name = htmltopdf
container_name = htmltopdf

.PHONY: all
all: clean

.PHONY: clean
clean:
	rm -f *.pdf
	@# rm -f *.html
	@#sudo docker system prune --all
	@#sudo docker builder prune --all

# app 실행
.PHONY: run
run:
	uvicorn htmltopdf:app --host=0.0.0.0 --port=38000 --reload

# Dockerfile 이미지 빌드
.PHONY: docker-build
docker-build:
	sudo docker build . -t ${image_name} -t ${image_name}:${version} --no-cache

# https://playwright.dev/docs/ci#docker
# 빌드된 Docker 이미지로 컨테이너 생성
.PHONY: docker-run
docker-run:
	sudo docker run --ipc=host --init -d --name ${container_name} -p 15000:38000 -v ${PWD}/logs:/app/logs:rw ${image_name}:${version}

# Docker 컨테이너 중지 및 삭제
.PHONY: docker-stop
docker-stop:
	sudo docker rm -f ${container_name}

# 실행 중인 Docker 컨테이너 로그 확인
.PHONY: docker-logs
docker-logs:
	sudo docker logs -f ${container_name}

# Docker 이미지 삭제
.PHONY: docker-rmi
docker-rmi:
	@# https://www.gnu.org/software/make/manual/html_node/Errors.html#Errors-in-Recipes
	@# To ignore errors in a recipe line, write a ‘-’ at the beginning of the line’s text (after the initial tab).
	-sudo docker rmi ${image_name}
	sudo docker rmi $$(sudo docker images '${image_name}' -a -q)

# Docker 이미지 레이어 확인
.PHONY: check-docker-layers
check-docker-layers:
	sudo docker history ${image_name}:${version}

# core.{number} 파일 확인
.PHONY: check-core
check-core:
	sudo docker exec -it ${container_name} ls -hal

.PHONY: check-memory
check-memory:
	./scripts/check_memory.sh
