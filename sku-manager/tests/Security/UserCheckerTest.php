<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Tests\Security;

use App\Entity\User;
use App\Exception\UserAuthException;
use App\Security\UserChecker;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

class UserCheckerTest extends KernelTestCase
{
    private UserChecker $userChecker;

    public function setUp()
    {
        parent::setUp();
        self::bootKernel();
        $this->userChecker = static::$kernel->getContainer()->get(UserChecker::class);
    }

    public function testCheckPreAuth()
    {
        $user = new User();
        $this->expectException(UserAuthException::class);
        $this->userChecker->checkPreAuth($user);
    }

    public function testCheckPostAuth()
    {
        $user = new User();
        $this->expectException(UserAuthException::class);
        $this->userChecker->checkPostAuth($user);
    }
}
