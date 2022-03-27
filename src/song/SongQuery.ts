class SongQuery {
    sql: string
    params: string[]

    constructor(chars: string, includes: boolean) {
        this.params = Array.from(chars.split('')).map((c) => {
            return `%${c}%`
        })
        const conditions = Array.from(this.params).map((c) => {
            return `chars ${includes ? '' : 'not'} like ?`
        })
        this.sql = `
        SELECT *
        FROM songs
        WHERE ${conditions.join(includes ? ' OR ' : ' AND ')}
        order by sales desc
        `
    }
}

export default SongQuery