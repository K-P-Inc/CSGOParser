import pg from 'pg';
const { Client } = pg;

class RDSClient {
  private client?: pg.Client;
  private inited: boolean = false;

  constructor() {}

  async setup() {
    this.client = new Client({
        host: "db",
        user: "postgres",
        database: "postgres",
        password: "superbotparser",
        port: 5432
    });
    await this.client.connect();
    // and never end client??
    this.inited = true;
  }

  destroy() {
    if (this.inited && this.client !== undefined) {
      this.client.end();
    }
  }

  public async query(query: string, queryArgs?: any[]) {
    if (!this.inited) {
      await this.setup();
    }
    if (this.client === undefined) {
      throw new Error("Client is undefined when querying");
    }
    return RDSClient.makeQuery(this.client, query, queryArgs);
  }

  static async makeQuery(client: pg.Client, query: string, queryArgs?: any[]) {
    try {
      // await client.connect();
      let promise = await client.query(query, queryArgs)
      return promise.rows;
    } catch (e) {
      const error = e as Error
      console.error(error.stack);
    } finally {
      // await client.end();
    }
  }

  // Get list of all users
  // note: same as parseUsers
  async getAllUsers() {
    let result = await this.query(`
      SELECT users.username, users.realname, companies.name as company, users.debug_mode, users.send_recordings, users.tgt_spk_id
      FROM users
      JOIN companies ON companies.id = users.company_id
      ORDER BY username ASC
    `)
    return result;
  }

}

export const rdsClient = new RDSClient();