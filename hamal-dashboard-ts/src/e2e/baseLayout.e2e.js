const { uniq } = require('lodash');
const RouterConfig = require('../../config/config').default.routes;

const BASE_URL = `http://localhost:${process.env.PORT || 8000}`;

const getBrowser = require('./getBrowser');

function formatter(routes, parentPath = '') {
  const fixedParentPath = parentPath.replace(/\/{1,}/g, '/');
  let result = [];
  routes.forEach((item) => {
    if (item.path) {
      result.push(`${fixedParentPath}/${item.path}`.replace(/\/{1,}/g, '/'));
    }
    if (item.routes) {
      result = result.concat(
        formatter(item.routes, item.path ? `${fixedParentPath}/${item.path}` : parentPath),
      );
    }
  });
  return uniq(result.filter((item) => !!item));
}

let browser;
let page;

beforeAll(async () => {
  browser = await getBrowser();
});

beforeEach(async () => {
  page = await browser.newPage();
  await page.goto(`${BASE_URL}`);
  await page.evaluate(() => {
    localStorage.setItem('antd-pro-authority', '["admin"]');
  });
});

describe('Hamal Dashboard E2E test', () => {
  const testPage = (path) => async () => {
    await page.goto(`${BASE_URL}${path}`);
    await page.waitForSelector('footer', {
      timeout: 2000,
    });
    const haveFooter = await page.evaluate(
      () => document.getElementsByTagName('footer').length > 0,
    );
    expect(haveFooter).toBeTruthy();
  };

  const routers = formatter(RouterConfig);
  routers.forEach((route) => {
    it(`test pages ${route}`, testPage(route));
  });
});

afterAll(() => {
  browser.close();
});
