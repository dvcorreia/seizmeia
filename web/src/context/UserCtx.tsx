import React, {createContext, useState, useEffect} from 'react'

export const UserCtx = createContext()

export const UserProvider = (props) => {
    const [token, setToken] = useState(localStorage.getItem("seizmeiaToken"))

    useEffect(() => {
        const fetchUser = async () => {
            const opts = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }
            }

            const res = await fetch("http://localhost/api/users/me", opts)
            
            if (!res.ok) {
                setToken(null)
            }

            localStorage.setItem("seizmeiaToken", token)
        }

        fetchUser()
    }, [token])

    return (
        <UserCtx.Provider value={[token, setToken]}>
            {props.children}
        </UserCtx.Provider>
    )
}

