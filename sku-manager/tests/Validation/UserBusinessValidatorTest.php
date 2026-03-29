<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Tests\Validation;

use App\Entity\System;
use App\Entity\User;
use App\Validation\UserBusinessValidator;
use DateInterval;
use DateTime;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

class UserBusinessValidatorTest extends KernelTestCase
{
    private UserBusinessValidator $userBusinessValidator;

    public function setUp()
    {
        parent::setUp();
        self::bootKernel();
        $this->userBusinessValidator = static::$kernel->getContainer()->get(UserBusinessValidator::class);
    }

    public function testCheckActive()
    {
        $user = new User();
        $user->setActive(true);
        $this->assertEquals(true, $this->userBusinessValidator->checkActive($user));

        $user2 = new User();
        $user2->setActive(false);
        $this->assertEquals(false, $this->userBusinessValidator->checkActive($user2));
    }

    public function testCheckPasswordSet()
    {
        $user = new User();
        $user->setPassword('password_placeholder');
        $this->assertEquals(true, $this->userBusinessValidator->checkPasswordSet($user));

        $user2 = new User();
        $this->assertEquals(false, $this->userBusinessValidator->checkPasswordSet($user2));
    }

    public function testCheckSystemAssigned()
    {
        $system = new System();
        $system->setActive(true);

        $user = new User();
        $user->setSystem($system);

        $this->assertEquals(true, $this->userBusinessValidator->checkSystemAssigned($user));

        $user2 = new User();
        $this->assertEquals(false, $this->userBusinessValidator->checkSystemAssigned($user2));
    }

    public function testCheckSystemAvailable()
    {
        $system = new System();
        $system->setActive(true);

        $user = new User();
        $user->setSystem($system);
        $this->assertEquals(true, $this->userBusinessValidator->checkSystemAvailable($user));

        $system2 = new System();
        $system2->setActive(false);
        $user2 = new User();
        $user2->setSystem($system2);
        $this->assertEquals(false, $this->userBusinessValidator->checkSystemAvailable($user2));

        $system3 = new System();
        $system3->setActive(true);
        $oldDate = new DateTime();
        $oldDate->sub(new DateInterval('PT3H'));
        $system3->setTerminateDate($oldDate);
        $user3 = new User();
        $user3->setSystem($system3);
        $this->assertEquals(false, $this->userBusinessValidator->checkSystemAvailable($user2));
    }

    public function testCheckFailedAttemptsLimit()
    {
        $user = new User();
        $user->setFailedAttempts(1);
        $this->assertEquals(true, $this->userBusinessValidator->checkFailedAttemptsLimit($user));

        $user2 = new User();
        $user2->setFailedAttempts(100);
        $this->assertEquals(false, $this->userBusinessValidator->checkFailedAttemptsLimit($user2));
    }

    public function testCheckLastChangePasswordRequestTtl()
    {
        $user = new User();
        $user->setConfirmationToken('token_placeholder');
        $newDate = new DateTime();
        $newDate->sub(new DateInterval('PT1H'));
        $user->setPasswordRequestedAt(new DateTime());
        $this->assertEquals(true, $this->userBusinessValidator->checkLastChangePasswordRequestTtl($user));

        $user2 = new User();
        $user2->setConfirmationToken('token_placeholder');
        $oldDate = new DateTime();
        $oldDate->sub(new DateInterval('PT3H'));
        $user->setPasswordRequestedAt($oldDate);
        $this->assertEquals(false, $this->userBusinessValidator->checkLastChangePasswordRequestTtl($user2));
    }
}
