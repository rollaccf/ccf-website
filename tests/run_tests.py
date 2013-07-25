import urllib2

import about_us, alumni, catalyst, housing, resources
#TODO: Add manage pages


def generate_tests():
    # test homepage
    yield "", None

    test_groups = [about_us, alumni, catalyst, housing, resources]

    for group in test_groups:
        for url, data in group.generate_tests():
            yield url, data


if __name__ == "__main__":
    base_url = "http://localhost:8080"
    success_count = 0
    failed_count = 0
    for url, data in generate_tests():
        try:
            opener = urllib2.build_opener()
            opener.addheaders.append(('Cookie', 'dev_appserver_login="test@example.com:True:185804764220139124118"'))
            response = opener.open(base_url + url, data)
            if response.code is not 200:
                print "%s (%s)" % (response.code, url)
                failed_count += 1
            else:
                success_count += 1
        except Exception as e:
            print "Exception %s (%s)" % (e, url)
            failed_count += 1

    print "{} / {} tests succeeded".format(success_count, success_count + failed_count)
