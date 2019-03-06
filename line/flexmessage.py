from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage,
    BubbleContainer, BoxComponent, TextComponent,
    MessageAction
)

        res = BubbleContainer(
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(
                        text="result"
                    ),
                    TextComponent(
                        text="アイロン",
                        action=MessageAction(
                            text="アイロン"
                        )
                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="hello", contents=res)
#            TextSendMessage(text=res)
        )
