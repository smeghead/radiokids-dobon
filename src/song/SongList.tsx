import React, { useEffect, useState } from "react";
import initSqlJs from 'sql.js'
import dbFile from '../../public/songs.db?url'
import wasm from '../../node_modules/sql.js/dist/sql-wasm.wasm?url'

const sqlPromise = initSqlJs({
    locateFile: (file: string) => `${wasm}/../${file}`
});
const initDb = async () => {
    const dataPromise = fetch(dbFile).then(res => res.arrayBuffer());
    const [SQL, buf] = await Promise.all([sqlPromise, dataPromise])
    return new SQL.Database(new Uint8Array(buf));
}

type Song = {
    id: string;
    title: string;
    artist: string;
    sales: Number;
}
type Props = {
    chars: string;
    includes: boolean;
}

const uniq = (array: string[]) => {
    return array.filter((elem, index, self) => self.indexOf(elem) === index);
}

function SongList(props: Props): JSX.Element {
    const [songs, setSongs] = useState<Song[]>([])
    useEffect(() => {
        const f = async () => {
            const chars = props.chars
            const includes = props.includes
            if (chars.length === 0) {
                setSongs([])
                return
            }
            const songs: Song[] = []
            const db = await initDb()
            const stmt = db.prepare("SELECT * FROM songs WHERE chars like $chars");
            const cs = uniq(chars.split('')).sort()
            stmt.bind({$chars: '%' + cs.join('%') + '%'})
            while (stmt.step()) {
                const record = stmt.getAsObject()
                songs.push({
                    id: record.id?.toString() ?? '',
                    title: record.title?.toString() ?? '',
                    artist: record.artist?.toString() ?? '',
                    sales: new Number(record.sales?.toString() ?? '0'),
                })
            }
            console.log('collected')
            setSongs(songs)
        }
        f()
    }, [props])

    return (
        <div className='box'>
            <ul>
                {songs.map((song) => <li key={song.id}>{song.title} {song.artist}</li>)}
            </ul>
        </div>
    )
}
export default SongList
