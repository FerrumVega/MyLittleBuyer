import config
import pyrogram
import time

if __name__ == "__main__":
    app = pyrogram.Client("MLB", api_id=config.API_ID, api_hash=config.API_HASH)
    app.run(use_qr=True)
    stable_gifts_data = app.invoke(pyrogram.raw.functions.payments.GetStarGifts(hash=0))

    while True:
        t = time.time()
        gifts_data = app.invoke(
            pyrogram.raw.functions.payments.GetStarGifts(hash=stable_gifts_data.hash)
        )
        if not isinstance(
            gifts_data,
            pyrogram.raw.types.payments.StarGiftsNotModified,
        ):
            stable_gifts_data = gifts_data
            for new_gift in stable_gifts_data.gifts:
                app.send_document(
                    "me", app.download_media(new_gift.sticker, in_memory=True)
                )
                new_gift_info = f"Вышел новый подарок\nСтоимость: {new_gift.price}\nЛимитированный: {new_gift.is_limited}"
                if new_gift.is_limited:
                    new_gift_info += (
                        f" ({new_gift.available_amount}/{new_gift.total_amount})"
                    )
                    try:
                        app.send_gift("me", new_gift.id)
                    except:
                        pass
                app.send_message(
                    "me",
                    f"{new_gift_info}\nОбработка длилась {time.time() - t} секунд",
                )
        else:
            app.send_message("me", time.time() - t)
            time.sleep(config.CHECK_DELAY)
