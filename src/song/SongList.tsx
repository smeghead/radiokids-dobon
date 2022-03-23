// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getDocs, getFirestore } from "firebase/firestore"
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAQXDO2Vf3LTyy3A7Uw5Srqyl1OYKmo8-0",
  authDomain: "radiokids-eed86.firebaseapp.com",
  projectId: "radiokids-eed86",
  storageBucket: "radiokids-eed86.appspot.com",
  messagingSenderId: "150855601405",
  appId: "1:150855601405:web:e241e0d37ceebe17890294",
  measurementId: "G-K6CZP95YNH"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);
const db = getFirestore();
import { collection, query, where } from "firebase/firestore";
import { useEffect, useState } from "react";
const songsRef = collection(db, "songs");

type Song = {
    id: string;
    title: string;
    artist: string;
}
function SongList(): JSX.Element {
    const [songs, setSongs] = useState<Song[]>([])
    useEffect(() => {
        const f = async () => {
            const q = query(songsRef, where("artist", "==", 'AKB48'));
            const querySnapshot = await getDocs(q);
            const songs: Song[] = []
            querySnapshot.forEach((doc) => {
                const song = doc.data()
                songs.push({
                    id: song.id,
                    title: song.title,
                    artist: song.artist,
                })
            });
            setSongs(songs)
        }
        f()
    }, [])

    return (
        <ul>
            {songs.map((song) => <li key={song.id}>{song.title} {song.artist}</li>)}
        </ul>
    )
}
export default SongList