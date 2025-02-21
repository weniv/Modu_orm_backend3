// [Next.js 프로젝트]
// pages/blog/index.js

import { useEffect, useState } from "react";

// 웹브라우저에 코드가 다운로드된 후에 수행.
function WhoamiPage() {
  const [message, setMessage] = useState("no message");

  // 컴포넌트 초기화 시에 1회만 실행.
  useEffect(() => {
    // 이 fetch 요청은 브라우저에서 수행됩니다.
    fetch("http://localhost:8000/blog/whoami/", { credentials: "include" })
      .then((response) => response.text())
      .then((responseText) => {
        setMessage(responseText);
      });
  }, []);

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