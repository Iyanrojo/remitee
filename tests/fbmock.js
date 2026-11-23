// Firebase simulado para las pruebas automáticas (sustituye a firebase-config.js en tests/smoke.py).
// Firestore en memoria, persistido en localStorage("mockdb"). Usuario de prueba: test@gmail.com (uid U1).
(function(){
  const load = () => JSON.parse(localStorage.getItem("mockdb")||"{}"), store = db => localStorage.setItem("mockdb", JSON.stringify(db));
  const user = {uid:"U1", email:"test@gmail.com", emailVerified:true, providerData:[{providerId:"google.com"}], reload:async()=>{}, getIdToken:async()=>"t", sendEmailVerification:async()=>{}};
  let cb = null;
  const auth = { currentUser:null, languageCode:"es",
    onAuthStateChanged(f){ cb=f; setTimeout(()=>{ if(localStorage.getItem("mockauth")){ auth.currentUser=user; f(user);} else f(null); },50); },
    signInWithPopup: async()=>{ localStorage.setItem("mockauth","1"); auth.currentUser=user; return {user}; },
    signInWithEmailAndPassword: async()=>{ localStorage.setItem("mockauth","1"); auth.currentUser=user; return {user}; },
    createUserWithEmailAndPassword: async()=>{ localStorage.setItem("mockauth","1"); auth.currentUser=user; return {user}; },
    sendPasswordResetEmail: async()=>{},
    signOut: async()=>{ localStorage.removeItem("mockauth"); auth.currentUser=null; cb&&cb(null); } };
  const clone = v => JSON.parse(JSON.stringify(v, (k,x) => x && x.__ts ? Date.now() : x));
  const doc = (col,id) => ({
    async get(){ const d=load()[col+"/"+id]; return {exists:!!d, data:()=>clone(d||{})}; },
    async set(v,o){ const db=load(); const k=col+"/"+id; db[k]=Object.assign(o&&o.merge?(db[k]||{}):{}, clone(v)); store(db); } });
  const query = c => ({ get: async()=>{ const db=load();
    const docs=Object.keys(db).filter(k=>k.startsWith(c+"/")).map(k=>({id:k.slice(c.length+1), data:()=>{ const d=clone(db[k]); const t=d.updatedAt||0; d.updatedAt={toMillis:()=>t}; return d; }}));
    return {forEach:f=>docs.forEach(f)}; } });
  const fs = () => ({ collection:c=>({ doc:id=>doc(c,id), orderBy:()=>({limit:()=>query(c)}) }) });
  fs.FieldValue = { serverTimestamp:()=>({__ts:1}) };
  window.firebase = { initializeApp(){}, auth:Object.assign(()=>auth,{GoogleAuthProvider:function(){}}), firestore:fs };
  window.REMITEE_FIREBASE = {apiKey:"test"};
})();
