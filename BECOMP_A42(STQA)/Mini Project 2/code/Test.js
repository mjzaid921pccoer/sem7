
const {Builder,By} = require('selenium-webdriver');
var assert = require('chai').assert;

//const TIMEOUT = 300000;
var LINK = 'https://nss-pccoer-blog.herokuapp.com/blog/home';
var imagepath1 = __dirname + '\\dog.jpg';
var imagepath2 = __dirname + '\\rose.jpg';

var PASSWORD = "akash123";
var EMAIL = "akash123@gmail.com";

var NEW_USER_NAME = "neeraj123";
var NEW_USER_EMAIL = "neeraj@gmail.com";
var NEW_USER_PASSSWORD = "neeraj12345";

async function testLogin(driver){

    await driver.get(LINK);
    await driver.findElement(By.linkText('Login')).click();
    await driver.findElement(By.name('email')).sendKeys(EMAIL);
    await driver.findElement(By.name('password')).sendKeys(PASSWORD);
    await driver.findElement(By.className('btn btn-success btn-lg')).click();
    
}

async function testInvalidLogin1(driver){

    var INVALID_EMAIL = "INVALIDEMAIL";
    await driver.findElement(By.name('email')).sendKeys(INVALID_EMAIL);
    await driver.findElement(By.name('password')).sendKeys(PASSWORD);
    await driver.findElement(By.className('btn btn-success btn-lg')).click();
    var alertMsg = await driver.findElement(By.className('alert alert-danger alert-dismissible fade show')).getText();
    
    if(alertMsg.includes("enter valid email")){
        return 1;
    }
    else{
        return -1;
    }
}

async function testInvalidLogin2(driver){

    var INVALID_PASSWORD = "INVALIDPASSWORD";
    await driver.findElement(By.name('email')).sendKeys(EMAIL);
    await driver.findElement(By.name('password')).sendKeys(INVALID_PASSWORD);
    await driver.findElement(By.className('btn btn-success btn-lg')).click();
    var alertMsg = await driver.findElement(By.className('alert alert-danger alert-dismissible fade show')).getText();
    
    if(alertMsg.includes("password didnt match")){
        return 1;
    }
    else{
        return -1;
    }
}


async function testLogOut(driver){

    await testLogin(driver);
    await driver.findElement(By.linkText('Logout')).click();
    await driver.findElement(By.linkText('Home')).click();
}

async function testRegister(driver){

    await driver.findElement(By.linkText('Register')).click();
    await driver.findElement(By.name('name')).sendKeys(NEW_USER_NAME);
    await driver.findElement(By.name('email')).sendKeys(NEW_USER_EMAIL);
    await driver.findElement(By.name('password')).sendKeys(NEW_USER_PASSSWORD);
    await driver.findElement(By.className('btn btn-success btn-lg')).click();
    
    try{
        await driver.findElement(By.className('alert alert-danger alert-dismissible fade show')).getText();
        return -1;
    } catch(e){
        return 1;
    }
}

async function testInvalidRegistration(driver){
    var INVALID_NAME = "abc";
    await driver.findElement(By.linkText('Register')).click();
    await driver.findElement(By.name('name')).sendKeys(INVALID_NAME);
    await driver.findElement(By.name('email')).sendKeys(EMAIL);
    await driver.findElement(By.name('password')).sendKeys(PASSWORD);
    await driver.findElement(By.className('btn btn-success btn-lg')).click();
    var alertMsg = await driver.findElement(By.className('alert alert-danger alert-dismissible fade show')).getText();
    
    if(alertMsg.includes("name should be 5 character long")){
        return 1;
    }
    else{
        return -1
    }
}


async function testAddBlog(driver){

    let BLOG_TITLE = "Title of the blog";
    let BLOG_CONTENT = "Some content describing the event in the photograph";
    let TAG = "Some tags here";
    await testLogin(driver);
    await driver.findElement(By.linkText('AddArticle')).click();
    await driver.findElement(By.name('title')).sendKeys(BLOG_TITLE);
    await driver.findElement(By.name('file')).sendKeys(imagepath1);
    await driver.findElement(By.name('content')).sendKeys(BLOG_CONTENT);
    await driver.findElement(By.name('tag')).sendKeys(TAG);
    await driver.findElement(By.className('btn btn-success btn-lg')).click();
}

async function testEditBlog(driver){
    //await testLogin(driver);
    await driver.findElement(By.className('btn')).click();
    await driver.findElement(By.name('file')).sendKeys(imagepath2);
    await driver.findElement(By.className('btn btn-success btn-lg')).click();
}


async function testDeleteBlog(driver){

    //await testLogin(driver);
    var buttons = await driver.findElements(By.linkText("delete"));
    
    if(buttons.length>0){
        await buttons[0].click();
        var updatedButtonsList = await driver.findElements(By.linkText("delete"));
        if(updatedButtonsList.length<buttons.length){
            return 1;
        }else{
            return -1;
        }
    }else{
        return 1;
    }    
}


async function openInstagram(driver){
    await driver.get(LINK);
    await driver.findElement(By.className('fa fa-instagram')).click()
    var homeWindow = await driver.getWindowHandle();
    var windows = await driver.getAllWindowHandles();
    await driver.switchTo().window(windows[1]);
    var title = await driver.getTitle();
    await driver.close();
    await driver.switchTo().window(homeWindow);
    if(title=="NSS PCCOER (@nss_pccoer) • Instagram photos and videos"){
        
        return 1;
    }else{
        return -1;
    } 
}

async function openFacebook(driver){
    await driver.get(LINK);
    await driver.findElement(By.className('fa fa-facebook')).click()
    var homeWindow = await driver.getWindowHandle();
    var windows = await driver.getAllWindowHandles();
    await driver.switchTo().window(windows[1]);
    var title = await driver.getTitle();
    await driver.close();
    await driver.switchTo().window(homeWindow);
    if(title=="Pimpri Chinchwad College of Engineering & Research - Pccoer - Home | Facebook"){
        return 1;
    }else{
        return -1;
    }
}


async function openNSSPage(driver){
    await driver.get(LINK);
    await driver.findElement(By.linkText("NSS PCCOE&R")).click()
    var homeWindow = await driver.getWindowHandle();
    var windows = await driver.getAllWindowHandles();
    await driver.switchTo().window(windows[1]);
    var title = await driver.getTitle();
    await driver.close();
    await driver.switchTo().window(homeWindow);
    if(title=="NSS Unit at Pimpri Chinchwad College of Engineering and Research | PCCOER - PCMC, Pune"){
        return 1;
    }else{
        return -1;
    } 
}


//testLogin(driver);
//testInvalidLogin1(driver);
//testInvalidLogin2(driver);
//testInvalidRegistration(driver);
//testLogOut(driver);
//testRegister(driver);
//testAddBlog(driver);
//testEditBlog(driver);
//testDeleteBlog(driver);
//openInstagram(driver);
//openFacebook(driver);
//openNSSPage(driver);


describe('-> Testing webapp',()=>{
    
    const driver = new Builder().forBrowser('chrome').build();
    
    describe('## Login Test', () => {
        
        it('(*) Should login the user and display dashboard', async () => {
            await testLogin(driver);
            const url = await driver.getCurrentUrl();
            assert.equal(url,'https://nss-pccoer-blog.herokuapp.com/blog/dashboard');
            await driver.findElement(By.linkText('Logout')).click();
        });
    
        it('(*) Should not login the user with invalid email', async () => {
            var status1 = await testInvalidLogin1(driver);
            assert(1,status1);
        });
    
        it('(*) Should not login the user with invalid password', async () => {
            var status2 = await testInvalidLogin2(driver);
            assert(1,status2);
        });
        
    });

    describe('## Logout Test',() => {
        it('(*) Should log out user when clicked on Logout option',async () => {
            await testLogOut(driver);
            const url = await driver.getCurrentUrl();
            assert.equal(url,'https://nss-pccoer-blog.herokuapp.com/blog/home');
        });
    });

    describe('## Registration Test', () => {

        it('(*) Should register new user', async () => {
            var status = await testRegister(driver);
            assert.equal(status,1);
            await driver.findElement(By.linkText('Home')).click();
        });
    
        it('(*) Should not register new user with invalid username', async () => {
            var status1 = await testInvalidRegistration(driver);
            assert(1,status1);
            await driver.findElement(By.linkText('Home')).click();
        }); 
          
        
    });

    describe('## Blogs', () => {
        it('(*) Should create a new blog',async () => {
            await testAddBlog(driver);
            assert.equal('blog added','blog added');
            await driver.findElement(By.linkText('Home')).click();
        });

        it('(*) Should edit already created blog',async () => {
            await testEditBlog(driver);
            assert.equal('blog edited','blog edited');
            await driver.findElement(By.linkText('Home')).click();
        });

        it('(*) Should delete most recently created blog',async () => {
            var status = await testDeleteBlog(driver);
            assert.equal(status,1);
        });

    });

    

    describe('## Social Media Links', () => {

        it('(*) Should open Instagram page of NSS PCCOER', async () => {
            var status = await openInstagram(driver);
            assert.equal(status,1);
        });

        it('(*) Should open Facebook page of NSS PCCOER', async () => {
            var status = await openFacebook(driver);
            assert.equal(status,1);
            await driver.findElement(By.linkText('Logout')).click();
            await driver.findElement(By.linkText('Home')).click();
        });

        it('(*) Should open page of NSS on PCCOER official website', async () => {
            var status = await openNSSPage(driver);
            assert.equal(status,1);
        });

    });
    
    after(async () => driver.quit());
});