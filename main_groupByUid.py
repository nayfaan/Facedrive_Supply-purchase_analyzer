import main


def mergeOrderItems(order_1, order_2):
    for x in order_2:
        if x in order_1:

            for item in order_1:
                if item == x:
                    temp_item = item

            order_1.remove(x)
            temp_item.qty += x.qty
            order_1.add(temp_item)

        else:
            order_1.add(x)

    return order_1


def groupByUid(pr):
    pr_uid = {}
    for x in pr:
        if not pr[x]["uid"] in pr_uid:
            pr_uid.update(
                {
                    pr[x]["uid"]: {
                        "u_name": pr[x]["u_name"],
                        "price": pr[x]["price"],
                        "prod": pr[x]["prod"],
                    }
                }
            )

        else:
            pr_uid[pr[x]["uid"]]["price"] += pr[x]["price"]
            pr_uid[pr[x]["uid"]]["prod"] = mergeOrderItems(
                pr_uid[pr[x]["uid"]]["prod"], pr[x]["prod"]
            )

    return pr_uid


def cleanName(pr):
    for x in pr:
        pr[x]["u_name"] = pr[x]["u_name"].replace("\n", " ").replace(",", "")
        for y in pr[x]["prod"]:
            y.name = y.name.replace(",", "")
    return pr


def print_csv(pr):
    print("uid,username,price,product")
    for x in pr:
        print(x, pr[x]["u_name"], pr[x]["price"], pr[x]["prod"], sep=",")


def main_groupByUid(low_limit=0, high_limit=2147483647):
    pr_n = main.main(low_limit, high_limit, False)

    pr_uid = groupByUid(pr_n)

    pr_uid = cleanName(pr_uid)

    print_csv(pr_uid)


if __name__ == "__main__":
    main_groupByUid()
