import React, { useContext, useState } from 'react';
import { UserCtx } from '../context/UserCtx';

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMsg, setErrorMsg] = useState("");
    const [, setToken] = useContext(UserCtx)

    const onSubmit = async (e: React.ChangeEvent<HTMLInputElement>): Promise<void> => {
        e.preventDefault()

        const params = new URLSearchParams()
        params.set("grant_type", "")
        params.set("username", username)
        params.set("password", password)
        params.set("scope", "me")
        params.set("client_id", "")
        params.set("client_secret", "")

        const opts = {
            method: "POST",
            headers: {
                "Content-type": "application/x-www-form-urlencoded"
            },
            body: params.toString()
        }
        
        const res = await fetch("http://localhost/token", opts)
        const data = await res.json()

        if (!res.ok) {
            setErrorMsg(data.detail)
            return
        }

        setToken(data.access_token)
    }

    return (
        <form onSubmit={onSubmit}>  
            <h2>Login</h2>
            <label>Username</label>
            <input type="text" name="username" onChange={e => setUsername(e.target.value)} value={username}/>

            <br />

            <label>Password</label>
            <input type="password" id="password" name="password" onChange={e => setPassword(e.target.value)} value={password}/>

            <br />

            {errorMsg ? <p>{errorMsg}</p> : ""}

            <button type="submit" value="login">Login</button>
        </form>
    )
}

export default Login