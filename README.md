# 1. 프로젝트 소개
- 금융 상품 데이터를 활용한 REST API Server 구축\
- 팀원
    | 팀원   | 역할               | github                                           |
    |--------|--------------------|--------------------------------------------------|
    | 김가희 | navigator         | https://github.com/gmlgml5023 |
    | 황예원 | driver     |  https://github.com/cakejuuu  |


<br>

# 2. Tools & FrameWork
- Django
- Django REST Framework
- Postman

<br>

# 3. 마주한 에러들

### 1) 요청 url에 오류가 있었다. 그냥 엉뚱한 곳으로 보낸 것.
```
500 Internal Server Error
The server has encountered a situation it does not know how to handle.
```


### 2) 해당 상품의 DepositOptions 역참조
```
deposit_options = deposit_products.depositoptions_set.all()
```
- 1:N 관계에서 1에서 N을 참조하는 것은 역참조이다 !!!
- 아무 생각 없이 objects.get() 으로 조회하려고 했다...
- 먼저 금융상품을 조회해서, 그에 해당하는 옵션값을 역참조를 통해 조회해와야 했다.


### 3) push를 하는 과정에서 모든 프로젝트 파일들이 날라갔다.

> 원인
1. 리모트와의 불일치: 처음 git push를 시도했을 때 "Updates were rejected because the remote contains work that you do not have locally"라는 오류 메시지가 나타났다.
    => 원격 저장소에 이미 존재하는 커밋이 있어서 로컬 브랜치가 원격 브랜치보다 뒤처져 있다는 뜻이다.
2. 병합 실패: 원격 브랜치의 README랑 로컬 브랜치의 README가 다른 것 때문 같아서 pull을 시도했지만 fatal: refusing to merge unrelated histories"라는 오류가 발생했다.
=> 로컬 저장소와 원격 저장소의 커밋 기록이 서로 다르기 때문에 자동으로 병합할 수 없었다.
3. 강제 리셋을 실행: git reset --hard origin/master 명령어를 실행하여 원격 저장소의 상태로 리셋했다.
    => 이 과정에서 프로젝트 파일들이 전부 사라졌다. 이 명령어는 현재 브랜치를 원격 저장소의 master 브랜치와 동일한 상태로 강제로 되돌리는 것이다. 즉, 로컬의 모든 변경사항이 삭제되고 원격 저장소의 상태로 초기화되었고, 이후 git revert를 시도했지만 올바른 커밋을 지정하지 않아서 실패했다.

> 해결
1. 리플로그 확인: git reflog를 통해 커밋 기록을 확인해 되돌아가고 싶은 커밋의 커밋아이디를 확인했다.

2. 소프트 리셋 사용: git reset --soft 9ad8061 명령어를 사용하여 특정 커밋(여기서는 "프로젝트 제출" 커밋) 상태로 되돌렸다. (소프트 리셋은 해당 커밋 이후의 변경사항을 스테이지 상태로 남겨두기 때문에, 필요한 파일들을 다시 커밋할 수 있게 해준다고 한다)

3. 새로운 원격 저장소에 푸시: 원래의 커밋 상태로 돌아가 파일들을 복구했고, 새로운 원격 저장소를 설정하고 푸시하여 최종적으로 변경 사항을 저장소에 반영했다.
