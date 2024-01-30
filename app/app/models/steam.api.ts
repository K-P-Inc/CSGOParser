
export async function getSteamUserData(steam_api_key: string, steam_id: string): Promise<any> {
    const response = await fetch(`http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=${steam_api_key}&steamids=${steam_id}`)
        .then(res => res.json())

    console.log(response)
    if (response.response && response.response.players && response.response.players.length > 0) {
        return {
            icon_url: response.response.players[0].avatarfull,
            steam_name: response.response.players[0].personaname
        }
    } else {
        throw new Error("User not found");
    }
}
