import requests
import re
import json


class Tistory():
    def __init__(self, **kwargs):
        if 'api_keys' in kwargs.keys():
            tistory_data_list = kwargs['api_keys']
        else:
            with open('api_keys.json', 'r') as fp:
                tistory_data_list = json.load(fp)['tistory']
        self.app_id = tistory_data_list[-1]['appId']
        self.callback_url = tistory_data_list[-1]['callbackUrl']
        self.user_id = tistory_data_list[-1]['userId']
        self.password = tistory_data_list[-1]['password']
        self.blogname = tistory_data_list[-1]['blogname']
        self.access_token = self.getAccessToken()

    def getAccessToken(self,):
        print('토큰 요청')
        login_url = 'https://www.tistory.com/auth/login'
        oauth_url = 'https://www.tistory.com/oauth/authorize'
        loginParams = {
            'redirectUrl': self.callback_url,
            'loginId': self.user_id,
            'password': self.password,
            'fp': 'mymackbook',
        }
        tokenParams = {
            'client_id': self.app_id,
            'redirect_uri': self.callback_url,
            'response_type': 'token'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
        rs = requests.session()
        r0 = rs.get(oauth_url, params=tokenParams)
        rs.post(login_url, headers=headers, data=loginParams)
        r2 = rs.get(oauth_url, params=tokenParams)
        if r0.url == r2.url:
            print("이메일 인증이 되었는지 확인하고, 다시 시도해주십쇼.")
            return None
        else:
            match = re.match(
                '(.*?)access_token=(?P<access_token>.*?)&state=', r2.url)
            gd = match.groupdict()
            access_token = gd['access_token']
            print('접근용 토큰: ' + access_token + '\n')
            return access_token

    def getList(self, m_page_num):
        print("글 목록 요청")
        url = f"https://www.tistory.com/apis/post/list?access_token={self.access_token}&output=json&blogName={self.blogname}&page={str(m_page_num)}"
        res = json.loads(requests.get(url).text)
        ts_res = res["tistory"]
        if ts_res["status"] == '200':
            print("✅  요청 성공")
            item = ts_res["item"]
            posts = item["posts"]
            print("티스토리 기본 URL: " + item["url"])
            print("독립도메인 URL: " + item["secondaryUrl"])
            print("현재 페이지: " + item["page"])
            print("페이지의 글 개수: " + item["count"])
            print("전체 글 수: " + item["totalCount"] + '\n')
            for post in posts:
                print("글 ID: " + post["id"])
                print("글 제목: " + post["title"])
                print("글 대표 주소: " + post["postUrl"])
                print("글 공개 단계 (0: 비공개, 15: 보호, 20: 발행): " +
                      post["visibility"])
                print("카테고리 ID: " + post["categoryId"])
                print("댓글 수: " + post["comments"])
                print("트랙백 수 " + post["trackbacks"])
                print("날짜 (YYYY-mm-dd HH:MM:SS): " + post["date"] + '\n')
            return ts_res
        else:
            print("❌  요청 실패")
            print("status: " + ts_res["status"])
            print("error message: " + ts_res["error_message"])
            return False

    def getPublishedPosts(self):
        m_published_posts = []
        print("Start getPublishedPosts")
        i = 1
        while i:
            #print("I'm in while")
            item = self.getList(i)
            if str(item).find("posts") != -1:
                posts = item["tistory"]["item"]["posts"]
                #print("Start Print Posts")
                # print(posts)
                for post in posts:
                    m_visibility = str(post.get("visibility"))
                    if m_visibility == "20":
                        # print("published")
                        # print(post)
                        m_published_posts.append(post)
            else:
                return m_published_posts
            i = i+1

    def getRead():
        # TODO: 글 읽기
        return

    def writePost(self, m_title, m_content, m_category, m_tag):
        print("Start writePost")
        # TODO: 글쓰기
        # blogName: Blog Name (필수)
        # title: 글 제목 (필수)
        # content: 글 내용
        # visibility: 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행)
        # category: 카테고리 아이디 (기본값: 0)
        # published: 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간)
        # slogan: 문자 주소
        # tag: 태그 (',' 로 구분)
        # acceptComment: 댓글 허용 (0, 1 - 기본값)
        # password: 보호글 비밀번호
        params = {
            'blogName': self.blogname,
            'title': m_title,
            'content': m_content,
            'tag': m_tag,
            'category': m_category,
            'visibility': '0',
            # 'published' : '',
            # 'slogan' : '',
            # 'acceptComment' : '1',
            # 'password' : '',
            'access_token': self.getAccessToken(),
            'output': 'json'
        }
        data = json.dumps(params)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        rd = requests.post(
            'https://www.tistory.com/apis/post/write', data=data, headers=headers)
        if rd.status_code == 200:
            print("글 작성 성공")
            item = json.loads(rd.text)
            print("글 id: " + item["tistory"]["postId"])
            print("글 주소: " + item["tistory"]["url"])
            return True
        else:
            print(rd.status_code)
            print(rd.text)
            item = json.loads(rd.text)
            print(rd.status_code)
            print(item["tistory"]["error_message"])
            return False

    def modifyPost():
        # TODO: 글수정
        return

    def attach(self, m_imgname):
        # TODO: 파일첨부
        print("Start attach")
        m_filepath = './img/'+m_imgname
        files = {'uploadedfile': open(m_filepath, 'rb')}
        params = {'access_token': self.getAccessToken(
        ), 'targetUrl': self.blogname, 'output': 'json'}
        rd = requests.post(
            'https://www.tistory.com/apis/post/attach', params=params, files=files)
        try:
            item = json.loads(rd.text)
            print(item["tistory"]["replacer"])
            print(item["tistory"]["url"])
            os.remove(m_filepath)
            return(item["tistory"]["replacer"])
        except:
            print("Success")
        return item["tistory"]["replacer"]

    def getCategoryList():
        # TODO: 카테고리 리스트
        return

    def getNewestComment():
        # TODO: 최근 댓글 목록 가져오기
        return

    def getCommnetList():
        # TODO:  댓글 목록
        return

    def writeCommnet():
        # TODO: 댓글 작성
        return

    def modifyCommnet():
        # TODO: 댓글 수정
        return

    def delComment():
        # TODO: 댓글 삭제
        return
