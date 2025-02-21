import { useContext, useEffect, useState, Fragment } from 'react'

import Login from './Auth/Login'
import SignIn from './Auth/SignIn'
import { UserCtx } from './context/UserCtx'

function App() {
  const [version, setVersion] = useState("")
  const [token,] = useContext(UserCtx)

  const getVersion = async () => {
    const opts = {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    }

    const res = await fetch("http://localhost:80/api/version", opts)
    if (!res.ok) {
      setVersion("???")
    }
    
    const data = await res.json()
    setVersion(data.version)
  }

  useEffect(() => {
    getVersion()
  }, [])

  return (
    <div>
      <h1>Welcome to Seizmeia Web</h1>
      <h4>version: {version}</h4>
      {token ? <p>Welcome {token}</p> : <Fragment><Login /> <SignIn /></Fragment>}
    </div>
  )
}

export default App
