[ 수업 준비 체크리스트 ]

1. 설정 / 앱 에서 Microsoft Visual Studio Code, Miniconda3를 제거합니다. 

2. 사용자계정 폴더의 .conda, .ipython, .vscode, miniconda3 폴더와 .condarc 파일을 제거합니다. 아울러 C:\Users\사용자계정\AppData\Roaming\Code 폴더도 제거합니다.

3. 공유폴더
https://bit.ly/451kxMU

4. OpenAI 개발자 플랫폼에서 다음 사항이 준비 되었는지 확인합니다.
https://platform.openai.com/
- OpenAI API 개발자 계정 크레딧 밸런스 확인 (최소 등록 금액 $5)
- secret key 생성 및 복사 (secret key 생성 시에만 복사 가능)  


[ 실습 환경 설정 ]

1. miniconda3를 설치합니다.

https://www.anaconda.com/docs/getting-started/miniconda/install#quick-command-line-install

윈도우즈 커맨드 프롬프트에서 다음 명령을 복사 후 실행합니다.
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o .\miniconda.exe
start /wait "" .\miniconda.exe /S
del .\miniconda.exe




2. 시작 > Miniconda3 (64-bit) > Anaconda Prompt (miniconda)를 실행합니다.

3. 패키지 다운로드를 위한 conda-forge 리포지토리  채널을 추가하고, 채널 우선 순위를 변경합니다.

conda config --show channels 
channels:
  - https://repo.anaconda.com/pkgs/main
  - https://repo.anaconda.com/pkgs/r
  - https://repo.anaconda.com/pkgs/msys2
  
conda config --add channels conda-forge && conda config --set channel_priority strict

conda config --show channels
  - conda-forge
  - https://repo.anaconda.com/pkgs/main
  - https://repo.anaconda.com/pkgs/r
  - https://repo.anaconda.com/pkgs/msys2

4. Conda 가상 환경(langchain_part_2)을 만들고 확인합니다.

conda create -n langchain_part_2 python=3.12 -y

conda info --envs                      
# conda environments:
#
base                         C:\Users\사용자계정\miniconda3
langchain_part_2     C:\Users\사용자계정\miniconda3\envs\langchain_part_2   

5.Conda 가상 환경(langchain_part_2)을 활성화 합니다.

conda activate langchain_part_2
(langchain_part_2) C:\Users\사용자계정>

6. Jupyter Notebook을 설치합니다.

conda install notebook -y

7. Anaconda Prompt (miniconda) 창을 닫습니다.

8. visual studio code를 설치합니다. 

https://code.visualstudio.com/Download

9. visual studio code를 실행합니다. 

10. 확장 탭(CTRL+SHIFT+X)을 선택합니다.

11. Korean Language Pack for Visual Studio Code 확장팩을 설치하고, 재실행 버튼을 눌러 visual studio code를 재실행합니다.

12. Python 확장팩을 설치합니다.

13. Jupyter 확장팩을 설치합니다.

14. 탐색기(CTRL+SHIFT+E)를 선택합니다. / “폴더 열기”를 누릅니다. / langchain_part_2 폴더를 생성합니다. / langchain_part_2 폴더를 클릭 후 “폴더 선택”을 누릅니다. / 이 폴더에 있는 파일의 작성자를 신뢰합니까? 라는 질문이 나오면  “예, 작성자를 신뢰합니다.”를 선택합니다.

15. 명령팔레트(CTRL+SHIFT+P)를 실행합니다. / Python: Select Interpreter를 선택합니다. Conda 가상환경 (langchain_part_2)을 선택합니다.  




[ 수업 종료 전 체크리스트 ]
1. 설정 / 앱 에서 Microsoft Visual Studio Code, Miniconda3를 제거합니다. 
2. 사용자계정 폴더의 .conda, .ipython, .vscode, miniconda3 폴더와 .condarc 파일을 제거합니다. C:\Users\사용자계정\AppData\Roaming\Code 폴더도 제거합니다.
3. 소스코드와 환경설정 파일(.env)이 있는 프로젝트 폴더(langchain_part_2)도 제거합니다.
