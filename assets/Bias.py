from pybit.unified_trading import HTTP
import time

class BiasClass(HTTP):
    """
    This class is used to get the bias count and number of buy and sell candles
    """

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.start_time = round((time.time() * 1000)- (1440 * 60 * 1000),-5)
        self.second_time = round((time.time() * 1000) - (2160 * 60 * 1000),-5)
        self.time_length = 720  # also run time of bot in minutes
        self.crypto = list(*args)

        self.session = HTTP(
            demo=True,
            timeout=3600,
            force_retry=True,
            api_key="3p3uITuUg1PFZQZiw0",
            api_secret="N5kaK08auFJ9d531AnYKsmGNtrDJOrlh1tee",
        )

        # coins information
        self.crypto_data = {
            self.crypto[y]: self.session.get_kline(
                category="linear",
                symbol=self.crypto[y],
                interval=1,
                end=self.start_time,
                limit=self.time_length,
            )
            .get("result")
            .get("list") + self.session.get_kline(
                category="linear",
                symbol=self.crypto[y],
                interval=1,
                end=self.second_time,
                limit=self.time_length,
            )
            .get("result")
            .get("list")
            for y in range(len(self.crypto))
        }

    def bias_count(self, count):
        bias_score = 0
        candle_count = self.time_length - 1  # iteration count
        while candle_count > 0:

            candle_0_59 = self.crypto_data[self.crypto[count]]
            candle_60 = candle_0_59[candle_count]
            candles_high = max([float(candle_0_59[a][2]) for a in range(candle_count)])
            candles_low = min([float(candle_0_59[a][3]) for a in range(candle_count)])

            # candle data

            candle_high = float(candle_60[2])
            candle_low = float(candle_60[3])
            candle_open = float(candle_60[1])
            candle_close = float(candle_60[4])

            # seconds = float(candle_60[0]) / 1000
            # candle_time = time.strftime( "%H:%M:%S %d/%m/%Y", time.localtime(seconds))

            def unit(n):
                if n >= 1:
                    if n < 3 and n > 0:
                        return n
                    elif n > 2 and n < 10:
                        return -1
                    else:
                        return unit(n / 10)
                else:
                    return unit(n * 10)

            # quantity = round(((unit(candle_low) * 100) / candle_low), 5) / 10
            Profit_value = (candle_low * 0.5) / (unit(candle_low) * 100)

            # strategies used are as follows; trap stategy, swing high/low
            # buy candle
            if (
                (candle_close > candle_open)
                and (candles_high > candle_high)
                and (candles_high < (Profit_value + candle_high))
            ):

                bias_score += 1

            # sell candle
            elif (
                (candle_close < candle_open)
                and (candles_low < candle_low)
                and (candles_low > (candle_low - Profit_value))
            ):

                bias_score -= 1

            candle_count -= 1  # iteration
        return bias_score

if __name__ ==" __main__":
    coins = sorted(["ETHUSDT", "AAVEUSDT", "SOLUSDT", "COMPUSDT", "BNBUSDT", "BTCUSDT", "BCHUSDT", "GNOUSDT"])
    BC = BiasClass(coins)

    for i in range(len(coins)):
        print(f"{coins[i]} bias score: {BC.bias_count(i)}")
