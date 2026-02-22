const { command, isPrivate } = require("../lib")
const { downloadMediaMessage } = require('@adiwajshing/baileys')
const fetch = require("node-fetch")
let img = 'https://i.ibb.co/fnqzVXY/966fc55242ca.jpg'
command(
	{
		pattern: 'sk ?(.*)',
		fromMe: true,
		desc: 'Forward Audio',
		type: 'user',
	},
	async (message, match) => {


    const anu = {
      key: {
        participant: '0@s.whatsapp.net',
        remoteJid: 'status@broadcast'
      },
      message: {
        orderMessage: {
          itemCount: 2023,
          status: 999,
          thumbnail: await (await fetch(img)).buffer(),
          surface: 999,
          message: 'Suhaid', orderTitle: 'Aғɪʏᴀ-Bᴏᴛ-Mᴅ ⚡', sellerJid: '0@s.whatsapp.net'
        }
      }
    }



    if (!match) {
      message.client.sendMessage("*Give Jid To forward*");
    } else {
      let jid = match
      let audio = await downloadMediaMessage(message.reply_message,
        'buffer',
        {},
        {
          // pass this so that baileys can request a reupload of media
          // that has been deleted
          reuploadRequest: message.client.updateMediaMessage
        }
      )

      if (!message.reply_message) {
        message.client.sendMessage("*Reply To Audio*")
      } else {

        message.client.sendMessage(jid, {
          audio: audio, mimetype: 'audio/mpeg', ptt: true, waveform: [59,160,70,3,70,160,59], contextInfo: {
            externalAdReply: {
              title: "🎀 Aғɪʏᴀ-Bᴏᴛ-Mᴅ 🎀",
              body: "I'ᴍ Bᴀᴄᴋ 👋🏻💃🏻",
              mediaType: 2,
              duration: 99999999,
              filesize: 999999999999,
              thumbnail: await (await fetch(img)).buffer(),
              mediaUrl: 'https://instagram.com/______suhaid',
              sourceUrl: 'https://instagram.com/______suhaid',
              showAdAttribution: true
            }
          }
        }, { quoted: anu })

      }

    }

  }
);
