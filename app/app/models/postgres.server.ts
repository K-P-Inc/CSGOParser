import pg from 'pg';
const { Client } = pg;

export class RDSClient {
  private client?: pg.Client;
  private inited: boolean = false;

  constructor() {}

  async setup() {
    this.client = new Client({
        host: process.env.POSTGRES_HOST,
        user: process.env.POSTGRES_USER,
        database: process.env.POSTGRES_DB,
        password: process.env.POSTGRES_PASSWORD,
        port: parseInt(process.env.POSTGRES_PORT || "5432")
    });
    await this.client.connect();
    // and never end client??
    this.inited = true;
  }

  async destroy() {
    if (this.inited && this.client !== undefined) {
      try {
        await this.client.end();
      } catch (e: any) {
        console.error("Error closing the client:", e.stack);
      }
    }
  }
  
  public async query(query: string, queryArgs?: any[]) {
    if (!this.inited) {
      await this.setup();
    }
    if (this.client === undefined) {
      throw new Error("Client is undefined when querying");
    }
    const result = await RDSClient.makeQuery(this.client, query, queryArgs);

    await this.destroy();

    return result;
  }

  static async makeQuery(client: pg.Client, query: string, queryArgs?: any[]) {
    try {
      let promise = await client.query(query, queryArgs)
      return promise.rows;
    } catch (e) {
      const error = e as Error
      console.error(error.stack);
    } finally {
    }
  }
}
