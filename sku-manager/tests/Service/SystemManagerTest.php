<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Tests\Service;

use App\DataFixtures\SystemFixture;
use App\Entity\System;
use App\Service\SystemManager;
use DateTimeImmutable;
use Exception;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;
use Symfony\Component\Validator\ConstraintViolationListInterface;

/**
 * Class UserService.
 */
class SystemManagerTest extends KernelTestCase
{
    public function setUp()
    {
        parent::setUp();
        self::bootKernel();

        $em = static::$kernel->getContainer()->get('doctrine')->getManager();
        $systemFixture = new SystemFixture();
        $systemFixture->load($em);
    }

    /**
     * @return SystemManager|object|null
     */
    public function testServiceInit()
    {
        $systemManager = static::$kernel->getContainer()->get(SystemManager::class);
        $this->assertInstanceOf(SystemManager::class, $systemManager);

        return $systemManager;
    }

    /**
     * @depends testServiceInit
     *
     * @param SystemManager $systemManager
     *
     * @return System
     *
     * @throws Exception
     */
    public function testGetNewSystem(SystemManager $systemManager)
    {
        $system = $systemManager->getNewSystem();
        $this->assertInstanceOf(System::class, $system);

        return $system;
    }

    /**
     * @depends testServiceInit
     *
     * @param SystemManager $systemManager
     */
    public function testValidateSystem(SystemManager $systemManager)
    {
        $system = new System();
        $system->setCreatedDate(new DateTimeImmutable());
        $system->setUpdatedDate(new DateTimeImmutable());
        $system->setName('sample-system-human-code');
        $system->setRegion('sample-system-region');
        $system->setActive(true);
        $system->setContact('system.contact@placeholder.test');

        $errors = $systemManager->validateSystem($system);
        $this->assertInstanceOf(ConstraintViolationListInterface::class, $errors);

        $this->assertNotCount(0, $errors);
    }
}
