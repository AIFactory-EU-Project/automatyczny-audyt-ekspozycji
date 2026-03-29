<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Tests\Service;

use App\Service\BrandManager;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

/**
 * Class UserService.
 */
class BrandManagerTest extends KernelTestCase
{
    public function setUp()
    {
        parent::setUp();
        self::bootKernel();
    }

    public function testServiceInit(): void
    {
        $brandManager = static::$kernel->getContainer()->get(BrandManager::class);
        $this->assertInstanceOf(BrandManager::class, $brandManager);
    }
}
