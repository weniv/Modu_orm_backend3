// [Next.js 프로젝트]
// pages/blog/index.js

// 요청을 받으면, 응답 생성 시에 서버 단에서 호출
export async function getServerSideProps(context) {
    // http://localhost:3000 에서의 쿠키를 API 요청에 활용
    const headers = {
      Cookie: context.req.headers.cookie,
    };
    console.log("headers: ", headers);
  
    const url = "http://localhost:8000/blog/whoami/";
    const response = await fetch(url, { headers });
    const responseText = `상태코드: ${response.status}
  
  ${await response.text()}`;
  
    // props로 전달한 값이 컴포넌트의 속성값으로 주입
    return { props: { message: responseText } };
  }
  
  // 웹브라우저에 코드가 다운로드된 후에 수행.
  function WhoamiPage({ message }) {
    return (
      <div>
        <h2>whoami</h2>
        <pre>{message}</pre>
        <hr />
        <small>by Next.js</small>
      </div>
    );
  }
  
  export default WhoamiPage;