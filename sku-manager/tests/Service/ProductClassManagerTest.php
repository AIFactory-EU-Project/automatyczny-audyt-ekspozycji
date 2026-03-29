<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Tests\Service;

use App\Service\ProductClassManager;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

/**
 * Class UserService.
 */
class ProductClassManagerTest extends KernelTestCase
{
    public function setUp()
    {
        parent::setUp();
        self::bootKernel();
    }

    public function testServiceInit(): void
    {
        $productClassManager = static::$kernel->getContainer()->get(ProductClassManager::class);
        $this->assertInstanceOf(ProductClassManager::class, $productClassManager);
    }
}
