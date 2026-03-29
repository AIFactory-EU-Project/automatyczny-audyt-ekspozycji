<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Tests\Service;

use App\Entity\User;
use App\Service\UserManager;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;
use Symfony\Component\Validator\ConstraintViolationListInterface;

/**
 * Class UserService.
 */
class UserManagerTest extends KernelTestCase
{
    public function setUp()
    {
        parent::setUp();
        self::bootKernel();
    }

    /**
     * @return UserManager|object|null
     */
    public function testServiceInit()
    {
        $userManager = static::$kernel->getContainer()->get(UserManager::class);
        $this->assertInstanceOf(UserManager::class, $userManager);

        return $userManager;
    }

    /**
     * @depends testServiceInit
     *
     * @param UserManager $userManager
     */
    public function testUpdatePassword(UserManager $userManager)
    {
        $plainPasswordValue = 'plain_password';
        $user = new User();
        $user->setPlainPassword($plainPasswordValue);
        $userManager->updatePassword($user);

        $this->assertEmpty($user->getPlainPassword());
        $this->assertNotEmpty($user->getPassword());
        $this->assertNotEquals($plainPasswordValue, $user->getPassword());
    }

    /**
     * @depends testServiceInit
     *
     * @param UserManager $userManager
     */
    public function testValidateUser(UserManager $userManager)
    {
        $user = new User();
        $errors = $userManager->validateUser($user);
        $this->assertInstanceOf(ConstraintViolationListInterface::class, $errors);

        $this->assertNotCount(0, $errors);
    }
}
