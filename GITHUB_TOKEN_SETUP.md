# GitHub 토큰 자동 설정 가이드

## 🎯 개요
평가용 GitHub 토큰이 자동으로 설정되어 사용자가 매번 입력할 필요가 없습니다.

## ✅ 자동 설정 방법
평가용 GitHub 토큰은 다음 파일에 설정되어 있습니다:
- `.env` 파일 (로컬)
- `.streamlit/secrets.toml` 파일 (Streamlit Cloud)

**보안상의 이유로 토큰은 Git에 커밋되지 않습니다.**

## 📋 토큰 로드 우선순위

프로그램은 다음 순서로 GitHub 토큰을 자동 로드합니다:

1. **Streamlit Secrets** (Streamlit Cloud용)
2. **환경 변수** `GITHUB_TOKEN`
3. **.env 파일**
4. **기본값** (평가용 토큰)

## 🚀 사용 방법

### 방법 1: 자동 사용 (권장)
아무것도 하지 않아도 기본 토큰이 자동으로 적용됩니다!

앱을 실행하면 사이드바에 다음 메시지가 표시됩니다:
```
✅ 평가용 키가 자동으로 설정되었습니다.
```

### 방법 2: 다른 토큰 사용
필요시 사이드바에서 다른 토큰을 입력할 수 있습니다:
1. 사이드바의 "🔑부여받은 키 설정" 섹션으로 이동
2. "다른 키를 사용하려면 입력해주세요" 필드에 새 토큰 입력
3. 자동으로 새 토큰이 적용됨

## 🛠️ 개발자용 설정

### 로컬 개발 환경

#### .env 파일 사용 (이미 설정됨)
프로젝트 루트에 `.env` 파일이 자동 생성되어 있습니다:
```bash
# .env
GITHUB_TOKEN=YOUR_GITHUB_TOKEN_HERE
```

**실제 토큰은 관리자에게 문의하세요.**

#### 환경 변수 사용
```bash
# Linux/Mac
export GITHUB_TOKEN="YOUR_GITHUB_TOKEN_HERE"

# Windows (PowerShell)
$env:GITHUB_TOKEN="YOUR_GITHUB_TOKEN_HERE"

# Windows (CMD)
set GITHUB_TOKEN=YOUR_GITHUB_TOKEN_HERE
```

### Streamlit Cloud 배포

Streamlit Cloud에서 자동으로 작동하도록 설정되어 있습니다:

1. Streamlit Cloud 대시보드에서 앱 선택
2. **Settings** > **Secrets** 클릭
3. 다음 내용 추가:
```toml
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"
```

**참고**: 실제 토큰은 관리자가 설정합니다.

## 🔒 보안

### .gitignore 설정
다음 파일들은 Git에 커밋되지 않도록 설정되어 있습니다:
- `.env` - 로컬 환경 변수 파일
- `.streamlit/secrets.toml` - Streamlit Secrets 파일

### 파일 구조
```
webapp/
├── .env                      # Git 무시됨 (로컬 환경 변수)
├── .streamlit/
│   └── secrets.toml         # Git 무시됨 (Streamlit Secrets)
├── .gitignore               # 보안 파일 제외 설정
└── src/
    └── app.py               # 토큰 자동 로드 로직 포함
```

## 🧪 테스트

### 토큰 작동 확인
1. 앱 실행: `streamlit run src/app.py`
2. 사이드바에서 "✅ 평가용 키가 자동으로 설정되었습니다." 메시지 확인
3. 식단 최적화 실행 후 "파일 업로드" 버튼 클릭
4. 성공 메시지 확인: "✅ 파일 업로드 완료!"

### 문제 해결
업로드 실패 시:
1. 토큰이 올바른지 확인
2. GitHub 토큰이 만료되지 않았는지 확인
3. 인터넷 연결 확인

## 📝 변경 이력

### 2025-10-19
- ✅ 기본 GitHub 토큰 자동 설정 구현
- ✅ 다중 소스 토큰 로드 (Streamlit Secrets, 환경 변수, .env)
- ✅ 사용자 인터페이스 개선 (자동 설정 표시)
- ✅ 보안 설정 (.gitignore)

## 💡 FAQ

**Q: 매번 토큰을 입력해야 하나요?**
A: 아니요! 기본 토큰이 자동으로 적용됩니다.

**Q: 다른 토큰을 사용하고 싶어요.**
A: 사이드바의 키 입력 필드에 새 토큰을 입력하면 됩니다.

**Q: Streamlit Cloud에서도 작동하나요?**
A: 네! 기본값이 설정되어 있어 별도 설정 없이 작동합니다.

**Q: 보안이 걱정됩니다.**
A: `.env`와 `secrets.toml` 파일은 Git에 커밋되지 않습니다. 안전합니다!

---

**작성일**: 2025-10-19  
**작성자**: AI Assistant
