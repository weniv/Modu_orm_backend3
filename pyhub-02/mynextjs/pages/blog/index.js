// [Next.js 프로젝트]
// pages/blog/index.js
//  주의: src 디렉토리가 아닙니다.

import { useState } from "react";

function WhoamiPage() {
  const [message, setMessage] = useState("no message");

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