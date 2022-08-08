import { BehaviorSubject } from 'rxjs';

const currentUserSubject = new BehaviorSubject(JSON.parse(localStorage.getItem('currentUser')));

export const authenticationService = {
    login,
    logout,
    currentUser: currentUserSubject.asObservable(),
    get currentUserValue () { return currentUserSubject.value }
};

async function login(username, password) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `grant_type=&username=${username}&password=${password}&scope=&client_id=&client_secret=`
    };
    // localStorage.setItem('currentUser', JSON.stringify({ username, password }));

    const response = await fetch('http://localhost/login', requestOptions);
    if (!response.ok) {
        throw new Error(
            `This is an HTTP error: The status is ${response.status}`
        );
    }
    const user = await response.json();
    user.username = username
    // store user details and jwt token in local storage to keep user logged in between page refreshes
    localStorage.setItem('currentUser', JSON.stringify(user));
    console.log(user);
    currentUserSubject.next(user);
    return user;
}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('currentUser');
    currentUserSubject.next(null);
}