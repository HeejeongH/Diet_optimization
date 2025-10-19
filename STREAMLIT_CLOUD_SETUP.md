# 🌐 Streamlit Cloud에서 GitHub 토큰 설정하기

## 📋 개요
Streamlit Cloud에서 앱을 배포할 때 GitHub 토큰을 안전하게 설정하는 방법입니다.

## 🔑 Streamlit Cloud Secrets 설정

### 1단계: Streamlit Cloud 접속
1. [https://share.streamlit.io/](https://share.streamlit.io/) 접속
2. 배포된 앱 선택

### 2단계: Secrets 메뉴 접근
1. 앱 대시보드에서 **⚙️ Settings** 클릭
2. **Secrets** 탭 선택

### 3단계: 토큰 설정
다음 내용을 Secrets 편집기에 입력:

```toml
GITHUB_TOKEN = "발급받은_실제_토큰을_여기에_입력"
```

**참고**: 실제 토큰은 별도로 제공되었습니다.

### 4단계: 저장 및 재시작
1. **Save** 버튼 클릭
2. 앱이 자동으로 재시작됩니다
3. 약 1-2분 후 앱에 다시 접속

## ✅ 설정 확인

앱이 재시작된 후:
1. 사이드바를 확인하세요
2. "✅ 평가용 키가 자동으로 설정되었습니다." 메시지가 표시되면 성공!

## 🎬 스크린샷 가이드

### Settings 버튼 위치
```
┌─────────────────────────────────────┐
│  [앱 이름]                          │
│  ┌────────┐  ┌────────┐  ⚙️         │
│  │ Reboot │  │ Delete │  Settings  │
│  └────────┘  └────────┘             │
└─────────────────────────────────────┘
```

### Secrets 편집기
```
Settings > Secrets

┌──────────────────────────────────────┐
│ # .streamlit/secrets.toml           │
│                                      │
│ GITHUB_TOKEN = "ghp_xxx..."         │
│                                      │
│                                      │
│                     [Cancel] [Save] │
└──────────────────────────────────────┘
```

## 🚨 주의사항

### 토큰 형식
- **올바른 형식**: `GITHUB_TOKEN = "ghp_..."`
- **잘못된 형식**: 
  - `GITHUB_TOKEN: "ghp_..."` (콜론 사용 X)
  - `github_token = "ghp_..."` (소문자 X)

### 따옴표 사용
- 반드시 큰따옴표(`"`)를 사용하세요
- 작은따옴표(`'`)는 사용하지 마세요

### 공백 주의
- 등호(`=`) 앞뒤에 공백이 있어도 됩니다
- 하지만 키 이름과 값에는 공백이 없어야 합니다

## 🔍 문제 해결

### 토큰이 적용되지 않는 경우
1. **Secrets 확인**
   - Settings > Secrets에서 올바르게 입력했는지 확인
   - 토큰 형식이 정확한지 확인

2. **앱 재시작**
   - Secrets 변경 후 반드시 앱 재시작 필요
   - Reboot 버튼 클릭 또는 자동 재시작 대기

3. **브라우저 캐시 삭제**
   - Ctrl+F5 (Windows) 또는 Cmd+Shift+R (Mac)로 새로고침

### 에러 메시지 확인
앱 하단의 "Manage app" 링크를 클릭하여 로그 확인:
```
Manage app > Logs
```

## 📱 모바일에서 설정

Streamlit Cloud는 모바일 웹에서도 접근 가능합니다:
1. 모바일 브라우저에서 share.streamlit.io 접속
2. 데스크톱 모드로 전환 (브라우저 설정에서)
3. 동일한 방법으로 Settings > Secrets 설정

## 🔐 보안 Best Practices

### 토큰 관리
- ✅ Streamlit Secrets에만 저장
- ✅ GitHub Repository Secrets와 분리
- ❌ 코드에 직접 하드코딩하지 않기
- ❌ 공개 채널에 공유하지 않기

### 토큰 권한
- 필요한 최소 권한만 부여
- 평가용 토큰의 경우: `repo` 권한만 있으면 충분

### 토큰 만료
- 정기적으로 토큰 갱신
- 만료된 토큰은 즉시 교체

## 💡 추가 팁

### 여러 환경 관리
- **개발**: `.env` 파일 사용
- **스테이징**: Streamlit Cloud Secrets (다른 앱)
- **프로덕션**: Streamlit Cloud Secrets (메인 앱)

### 팀 협업
- 팀원에게 Streamlit Cloud 접근 권한 부여
- Settings > Sharing에서 협업자 추가

## 📚 참고 자료

- [Streamlit Secrets 공식 문서](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [GitHub Personal Access Token 생성](https://github.com/settings/tokens)

---

**작성일**: 2025-10-19  
**작성자**: AI Assistant

**참고**: 실제 평가용 토큰은 `.env` 파일 또는 Streamlit Cloud Secrets에서 확인하세요.
