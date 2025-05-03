import argparse
import datetime
import sys

from scrapy.cmdline import execute

if __name__ == "__main__":
    # コマンドライン引数設定
    parser = argparse.ArgumentParser(
        usage="\n"
        + "集計したいaucfunの検索結果ページを指定して、商品情報を取得します。\n"
        + "取得した情報はcsv形式で保存されます。\n\n"
        + "例:\n"
        + "python scraper <aucfunの検索結果ページurl> -N <ページ数>",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("url", type=str, help="aucfunの検索結果ページurlを入力します")
    parser.add_argument(
        "-N",
        "--num",
        type=int,
        default=1,
        help="取得する最大ページ数 (デフォルト：1)",
    )
    parser.add_argument(
        "-L",
        "--loglevel",
        default="INFO",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    args = parser.parse_args()

    # 保存するcsvファイル名
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_aucfun.csv"

    if len(sys.argv) < 2:
        print(
            "aucfunの検索結果ページurlを入力してください。最大ページ数も指定できます。"
        )
        print('例：python scraper "https://aucfan.com/search1/..." -N <ページ数>')

        sys.exit(1)

    url = sys.argv[1]

    # スクレイピング実行
    cmd = [
        "scrapy",
        "crawl",
        "aucfun",
        "-o",
        filename,
        "-L",
        args.loglevel,
        "-a",
        "url=" + url,
        "-a",
        "num=" + str(args.num),
    ]
    print(" ".join(cmd))
    execute(cmd)
