<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Tests\Service;

use App\Service\TrainingManager;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

/**
 * Class UserService.
 */
class TrainingManagerTest extends KernelTestCase
{
    public function setUp()
    {
        parent::setUp();
        self::bootKernel();
    }

    public function testServiceInit(): void
    {
        $trainingManager = static::$kernel->getContainer()->get(TrainingManager::class);
        $this->assertInstanceOf(TrainingManager::class, $trainingManager);
    }
}
